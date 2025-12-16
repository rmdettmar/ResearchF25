import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.IDLE = 0
        self.SHIFT = 1
        self.COUNT = 2
        self.DONE = 3

        # Initialize state registers
        self.current_state = self.IDLE
        self.pattern_reg = 0  # Stores last 4 bits
        self.shift_counter = 0  # Counter for SHIFT state

        # Initialize outputs
        self.shift_ena = 0
        self.counting = 0
        self.done = 0

    def load(self, stimulus_dict: Dict[str, any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals
            reset = int(stimulus["reset"], 2)
            data = int(stimulus["data"], 2)
            done_counting = int(stimulus["done_counting"], 2)
            ack = int(stimulus["ack"], 2)

            # Reset logic
            if reset:
                self.current_state = self.IDLE
                self.pattern_reg = 0
                self.shift_counter = 0
                self.shift_ena = 0
                self.counting = 0
                self.done = 0
            else:
                # State machine logic
                if self.current_state == self.IDLE:
                    self.shift_ena = 0
                    self.counting = 0
                    self.done = 0
                    # Shift in new bit and check pattern
                    self.pattern_reg = ((self.pattern_reg << 1) | data) & 0xF
                    if self.pattern_reg == 0b1101:
                        self.current_state = self.SHIFT
                        self.shift_counter = 0
                        self.shift_ena = 1

                elif self.current_state == self.SHIFT:
                    self.shift_counter += 1
                    if self.shift_counter >= 4:
                        self.current_state = self.COUNT
                        self.shift_ena = 0
                        self.counting = 1

                elif self.current_state == self.COUNT:
                    if done_counting:
                        self.current_state = self.DONE
                        self.counting = 0
                        self.done = 1

                elif self.current_state == self.DONE:
                    if ack:
                        self.current_state = self.IDLE
                        self.done = 0
                        self.pattern_reg = 0

            # Format outputs as binary strings
            output_dict = {
                "shift_ena": format(self.shift_ena, "b"),
                "counting": format(self.counting, "b"),
                "done": format(self.done, "b"),
            }
            output_list.append(output_dict)

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
