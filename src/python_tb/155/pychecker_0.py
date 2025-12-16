import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.walking_left = True  # True for left, False for right
        self.falling = False

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            bump_left = BinaryValue(stimulus["bump_left"]).integer
            bump_right = BinaryValue(stimulus["bump_right"]).integer
            ground = BinaryValue(stimulus["ground"]).integer

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
                self.falling = False
            else:
                # Update falling state
                self.falling = ground == 0

                # Update walking direction only if not falling and ground present
                if not self.falling and ground:
                    if bump_left and not bump_right:
                        self.walking_left = False
                    elif bump_right and not bump_left:
                        self.walking_left = True
                    elif bump_left and bump_right:
                        self.walking_left = not self.walking_left

            # Set outputs
            walk_left = "1" if self.walking_left and not self.falling else "0"
            walk_right = "1" if not self.walking_left and not self.falling else "0"
            aaah = "1" if self.falling else "0"

            # Add outputs to stimulus_outputs
            output_dict = {
                "walk_left": walk_left,
                "walk_right": walk_right,
                "aaah": aaah,
            }
            stimulus_outputs.append(output_dict)

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
