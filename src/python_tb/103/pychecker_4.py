import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.STATE_A = 0  # 000
        self.STATE_B = 1  # 001
        self.STATE_C = 2  # 010
        self.STATE_D = 3  # 011
        self.STATE_E = 4  # 100
        self.STATE_F = 5  # 101

        # Initialize state register
        self.current_state = self.STATE_A

    def calculate_next_state(self, state, w):
        if state == self.STATE_A:
            return self.STATE_B if w else self.STATE_A
        elif state == self.STATE_B:
            return self.STATE_C if w else self.STATE_D
        elif state == self.STATE_C:
            return self.STATE_E if w else self.STATE_D
        elif state == self.STATE_D:
            return self.STATE_F if w else self.STATE_A
        elif state == self.STATE_E:
            return self.STATE_E if w else self.STATE_D
        elif state == self.STATE_F:
            return self.STATE_C if w else self.STATE_D
        return self.STATE_A

    def calculate_output(self, state):
        return 1 if state in [self.STATE_E, self.STATE_F] else 0

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to values
            reset_bv = BinaryValue(stimulus["reset"])
            w_bv = BinaryValue(stimulus["w"])

            reset = reset_bv.integer
            w = w_bv.integer

            # Handle reset
            if reset:
                self.current_state = self.STATE_A
            else:
                # Calculate next state
                self.current_state = self.calculate_next_state(self.current_state, w)

            # Calculate output
            z = self.calculate_output(self.current_state)

            # Convert output to binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            outputs.append({"z": z_bv.binstr})

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
