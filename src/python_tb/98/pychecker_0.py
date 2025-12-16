import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # FSM States
        self.STATE_A = 0  # Reset state
        self.STATE_B = 1  # f=1 state
        self.STATE_C = 2  # Monitor x state
        self.STATE_D = 3  # Monitor y state
        self.STATE_G1 = 4  # Final state g=1
        self.STATE_G0 = 5  # Final state g=0

        # Initialize state registers
        self.current_state = self.STATE_A
        self.x_pattern = [0, 0, 0]  # Store last 3 x values
        self.y_counter = 0  # Counter for y monitoring
        self.f_out = 0
        self.g_out = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            resetn = BinaryValue(stimulus["resetn"]).integer
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # State machine logic
            if not resetn:
                self.current_state = self.STATE_A
                self.x_pattern = [0, 0, 0]
                self.y_counter = 0
                self.f_out = 0
                self.g_out = 0
            else:
                if self.current_state == self.STATE_A:
                    self.current_state = self.STATE_B
                    self.f_out = 1

                elif self.current_state == self.STATE_B:
                    self.current_state = self.STATE_C
                    self.f_out = 0

                elif self.current_state == self.STATE_C:
                    # Update x pattern
                    self.x_pattern = [x] + self.x_pattern[:-1]
                    if self.x_pattern == [1, 0, 1]:
                        self.current_state = self.STATE_D
                        self.g_out = 1

                elif self.current_state == self.STATE_D:
                    if y == 1:
                        self.current_state = self.STATE_G1
                    else:
                        self.y_counter += 1
                        if self.y_counter >= 2:
                            self.current_state = self.STATE_G0
                            self.g_out = 0

                elif self.current_state == self.STATE_G1:
                    self.g_out = 1

                elif self.current_state == self.STATE_G0:
                    self.g_out = 0

            # Prepare output dictionary
            output_list.append(
                {"f": format(self.f_out, "b"), "g": format(self.g_out, "b")}
            )

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


def check_output(stimulus_list):

    dut = GoldenDUT()
    tb_outputs = []

    for stimulus in stimulus_list:

        tb_outputs.append(dut.load(stimulus))

    return tb_outputs


if __name__ == "__main__":

    with open("stimulus.json", "r") as f:
        stimulus_data = json.load(f)

    if isinstance(stimulus_data, dict):
        stimulus_list = stimulus_data.get("input variable", [])
    else:
        stimulus_list = stimulus_data

    outputs = check_output(stimulus_list)

    print(json.dumps(outputs, indent=2))
