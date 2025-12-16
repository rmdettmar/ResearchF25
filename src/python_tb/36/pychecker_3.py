import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize counter state to weakly not-taken (01)
        self.state = 1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings to integers
            areset = BinaryValue(stimulus["areset"]).integer
            train_valid = BinaryValue(stimulus["train_valid"]).integer
            train_taken = BinaryValue(stimulus["train_taken"]).integer

            # Handle asynchronous reset
            if areset:
                self.state = 1  # Reset to weakly not-taken (01)
            # Update counter based on training signals
            elif train_valid:
                if train_taken:
                    # Increment with saturation at 3
                    self.state = min(3, self.state + 1)
                else:
                    # Decrement with saturation at 0
                    self.state = max(0, self.state - 1)

            # Convert state to 2-bit binary string for output
            state_bv = BinaryValue(value=self.state, n_bits=2)
            stimulus_outputs.append({"state": state_bv.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
