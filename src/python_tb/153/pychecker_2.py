import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize states
        self.walking_left = True  # True for left, False for right
        self.is_falling = False
        self.is_digging = False

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs from binary strings to boolean/int
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
                # Priority 1: Check falling condition
                if not ground:
                    self.is_falling = True
                    self.is_digging = False
                elif self.is_falling:  # Ground appeared after falling
                    self.is_falling = False
                # Priority 2: Check digging condition
                elif not self.is_falling and dig and ground and not self.is_digging:
                    self.is_digging = True
                elif self.is_digging and not ground:  # Finished digging
                    self.is_digging = False
                    self.is_falling = True
                # Priority 3: Handle direction changes (only when walking)
                elif not self.is_falling and not self.is_digging:
                    if bump_left:
                        self.walking_left = False
                    elif bump_right:
                        self.walking_left = True

            # Generate outputs
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
