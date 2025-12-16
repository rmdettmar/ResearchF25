import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # States
        self.STATE_A = 0
        self.STATE_B1 = 1
        self.STATE_B2 = 2
        self.STATE_B3 = 3

        # Initialize state variables
        self.current_state = self.STATE_A
        self.w_count = 0
        self.z_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            reset_bv = BinaryValue(stimulus["reset"])
            s_bv = BinaryValue(stimulus["s"])
            w_bv = BinaryValue(stimulus["w"])

            # Get integer values
            reset = reset_bv.integer
            s = s_bv.integer
            w = w_bv.integer

            # State machine logic
            if reset:
                self.current_state = self.STATE_A
                self.w_count = 0
                self.z_reg = 0
            else:
                if self.current_state == self.STATE_A:
                    if s:
                        self.current_state = self.STATE_B1
                        self.w_count = 1 if w else 0
                        self.z_reg = 0
                elif self.current_state == self.STATE_B1:
                    self.current_state = self.STATE_B2
                    self.w_count += 1 if w else 0
                    self.z_reg = 0
                elif self.current_state == self.STATE_B2:
                    self.current_state = self.STATE_B3
                    self.w_count += 1 if w else 0
                    self.z_reg = 0
                else:  # STATE_B3
                    self.current_state = self.STATE_B1
                    self.z_reg = 1 if self.w_count == 2 else 0
                    self.w_count = 1 if w else 0

            # Add output to list
            stimulus_outputs.append(
                {"z": BinaryValue(value=self.z_reg, n_bits=1).binstr}
            )

        return {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }


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
