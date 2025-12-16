import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register to weakly not-taken (2'b01)
        self.state_reg = 1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals
            areset = int(BinaryValue(stimulus["areset"]).value)
            train_valid = int(BinaryValue(stimulus["train_valid"]).value)
            train_taken = int(BinaryValue(stimulus["train_taken"]).value)

            # Handle asynchronous reset
            if areset:
                self.state_reg = 1  # Reset to weakly not-taken (2'b01)
            elif train_valid:
                if train_taken:
                    # Increment with saturation at 3
                    self.state_reg = min(self.state_reg + 1, 3)
                else:
                    # Decrement with saturation at 0
                    self.state_reg = max(self.state_reg - 1, 0)

            # Format output as 2-bit binary string
            state_bv = BinaryValue(value=self.state_reg, n_bits=2)
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
