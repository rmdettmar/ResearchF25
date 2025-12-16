import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register - start walking left
        self.walking_left = True

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            bump_left = BinaryValue(stimulus["bump_left"]).integer
            bump_right = BinaryValue(stimulus["bump_right"]).integer

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
            else:
                # State transition logic
                if bump_left or bump_right:
                    self.walking_left = not self.walking_left

            # Create output dictionary for this cycle
            output = {
                "walk_left": "1" if self.walking_left else "0",
                "walk_right": "0" if self.walking_left else "1",
            }
            stimulus_outputs.append(output)

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
