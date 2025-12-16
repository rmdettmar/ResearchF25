import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register
        # Start walking left (1 for left, 0 for right)
        self.walking_left = True

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            areset = BinaryValue(stimulus["areset"]).integer
            bump_left = BinaryValue(stimulus["bump_left"]).integer
            bump_right = BinaryValue(stimulus["bump_right"]).integer

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
            else:
                # Update state based on bump inputs
                if bump_left and not bump_right:
                    self.walking_left = False
                elif bump_right and not bump_left:
                    self.walking_left = True
                elif bump_left and bump_right:
                    self.walking_left = not self.walking_left

            # Generate outputs based on current state
            walk_left = "1" if self.walking_left else "0"
            walk_right = "0" if self.walking_left else "1"

            # Add outputs to results
            stimulus_outputs.append({"walk_left": walk_left, "walk_right": walk_right})

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
