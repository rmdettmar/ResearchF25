import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state - walking left by default
        """
        self.walking_left = True  # True = walking left, False = walking right

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Update state based on input signals and return outputs
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            areset = BinaryValue(stimulus["areset"]).integer
            bump_left = BinaryValue(stimulus["bump_left"]).integer
            bump_right = BinaryValue(stimulus["bump_right"]).integer

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
            else:
                # Update state based on bump signals
                if bump_left and not bump_right:
                    self.walking_left = False
                elif bump_right and not bump_left:
                    self.walking_left = True
                elif bump_left and bump_right:
                    self.walking_left = not self.walking_left

            # Generate outputs based on current state
            output_dict = {
                "walk_left": "1" if self.walking_left else "0",
                "walk_right": "0" if self.walking_left else "1",
            }
            outputs.append(output_dict)

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
