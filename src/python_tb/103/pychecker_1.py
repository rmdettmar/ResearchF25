import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State definitions
        self.STATE_A = 0
        self.STATE_B = 1
        self.STATE_C = 2
        self.STATE_D = 3
        self.STATE_E = 4
        self.STATE_F = 5

        # Initialize current state
        self.current_state = self.STATE_A

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs from binary strings to integers
            reset = BinaryValue(stimulus["reset"]).integer
            w = BinaryValue(stimulus["w"]).integer

            # Handle state transitions
            if reset:
                next_state = self.STATE_A
            else:
                if self.current_state == self.STATE_A:
                    next_state = self.STATE_B if w else self.STATE_A
                elif self.current_state == self.STATE_B:
                    next_state = self.STATE_C if w else self.STATE_D
                elif self.current_state == self.STATE_C:
                    next_state = self.STATE_E if w else self.STATE_D
                elif self.current_state == self.STATE_D:
                    next_state = self.STATE_F if w else self.STATE_A
                elif self.current_state == self.STATE_E:
                    next_state = self.STATE_E if w else self.STATE_D
                else:  # STATE_F
                    next_state = self.STATE_C if w else self.STATE_D

            # Update current state
            self.current_state = next_state

            # Generate output z
            z = 1 if self.current_state in [self.STATE_E, self.STATE_F] else 0

            # Convert output to binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            stimulus_outputs.append({"z": z_bv.binstr})

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
