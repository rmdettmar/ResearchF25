import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to A (0)
        self.current_state = 0
        # State encodings
        self.STATE_A = 0
        self.STATE_B = 1
        self.STATE_C = 2
        self.STATE_D = 3
        self.STATE_E = 4
        self.STATE_F = 5

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to appropriate types
            reset_bv = BinaryValue(stimulus["reset"])
            w_bv = BinaryValue(stimulus["w"])
            reset = reset_bv.integer
            w = w_bv.integer

            # Update state based on reset and inputs
            if reset:
                self.current_state = self.STATE_A
            else:
                # State transition logic
                if self.current_state == self.STATE_A:
                    self.current_state = self.STATE_B if w else self.STATE_A
                elif self.current_state == self.STATE_B:
                    self.current_state = self.STATE_C if w else self.STATE_D
                elif self.current_state == self.STATE_C:
                    self.current_state = self.STATE_E if w else self.STATE_D
                elif self.current_state == self.STATE_D:
                    self.current_state = self.STATE_F if w else self.STATE_A
                elif self.current_state == self.STATE_E:
                    self.current_state = self.STATE_E if w else self.STATE_D
                elif self.current_state == self.STATE_F:
                    self.current_state = self.STATE_C if w else self.STATE_D

            # Output logic - z is 1 in states E and F
            z = 1 if self.current_state in [self.STATE_E, self.STATE_F] else 0

            # Convert output to BinaryValue and then to string
            z_bv = BinaryValue(value=z, n_bits=1)
            output_list.append({"z": z_bv.binstr})

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
