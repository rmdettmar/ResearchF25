import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers:
        - walking_left: tracks walking direction
        - is_falling: tracks falling state
        - is_digging: tracks digging state
        """
        self.walking_left = True  # Start walking left
        self.is_falling = False
        self.is_digging = False

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])
            dig = int(stimulus["dig"])

            # Handle reset
            if areset:
                self.walking_left = True
                self.is_falling = False
                self.is_digging = False
            else:
                # Priority 1: Check falling state
                if not ground:
                    self.is_falling = True
                    self.is_digging = False
                elif self.is_falling:  # Landing
                    self.is_falling = False
                # Priority 2: Check digging state
                elif not self.is_falling and ground and dig and not self.is_digging:
                    self.is_digging = True
                elif self.is_digging and not ground:
                    self.is_digging = False
                    self.is_falling = True
                # Priority 3: Handle direction changes
                elif not self.is_falling and not self.is_digging:
                    if bump_left and not bump_right:
                        self.walking_left = False
                    elif bump_right and not bump_left:
                        self.walking_left = True
                    elif bump_left and bump_right:
                        self.walking_left = not self.walking_left

            # Generate outputs
            output = {
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
