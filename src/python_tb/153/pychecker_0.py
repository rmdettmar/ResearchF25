import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.walking_left = True  # True for left, False for right
        self.is_falling = False
        self.is_digging = False

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to boolean
            areset = bool(int(stimulus["areset"]))
            bump_left = bool(int(stimulus["bump_left"]))
            bump_right = bool(int(stimulus["bump_right"]))
            ground = bool(int(stimulus["ground"]))
            dig = bool(int(stimulus["dig"]))

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
                self.is_falling = False
                self.is_digging = False
            else:
                # Update falling state
                if not ground:
                    self.is_falling = True
                    self.is_digging = False
                elif self.is_falling:
                    self.is_falling = False

                # Update digging state if not falling
                if not self.is_falling and ground and dig and not self.is_digging:
                    self.is_digging = True
                elif self.is_digging and not ground:
                    self.is_digging = False
                    self.is_falling = True

                # Update walking direction if not falling or digging
                if not self.is_falling and not self.is_digging:
                    if bump_left:
                        self.walking_left = False
                    elif bump_right:
                        self.walking_left = True

            # Prepare outputs
            outputs = {
                "walk_left": (
                    "1"
                    if self.walking_left and not self.is_falling and not self.is_digging
                    else "0"
                ),
                "walk_right": (
                    "1"
                    if not self.walking_left
                    and not self.is_falling
                    and not self.is_digging
                    else "0"
                ),
                "aaah": "1" if self.is_falling else "0",
                "digging": "1" if self.is_digging else "0",
            }

            stimulus_outputs.append(outputs)

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
