import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.walking_left = True  # True for left, False for right
        self.falling = False
        self.fall_counter = 0
        self.digging = False
        self.splattered = False

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to boolean/int
            bump_left = int(stimulus["bump_left"], 2)
            bump_right = int(stimulus["bump_right"], 2)
            ground = int(stimulus["ground"], 2)
            dig = int(stimulus["dig"], 2)

            # Skip state updates if splattered
            if not self.splattered:
                # Handle falling state
                if not ground:
                    if not self.falling:
                        self.falling = True
                        self.fall_counter = 0
                    else:
                        self.fall_counter += 1
                elif self.falling:  # Landing
                    self.falling = False
                    if self.fall_counter > 20:
                        self.splattered = True

                # Handle digging state
                if not self.falling and ground and dig and not self.digging:
                    self.digging = True
                elif self.digging and not ground:
                    self.digging = False
                    self.falling = True
                    self.fall_counter = 0

                # Handle direction changes
                if not self.falling and not self.digging:
                    if bump_left and not bump_right:
                        self.walking_left = False
                    elif bump_right and not bump_left:
                        self.walking_left = True
                    elif bump_left and bump_right:
                        self.walking_left = not self.walking_left

            # Generate outputs
            outputs = {
                "walk_left": (
                    "1"
                    if not self.splattered
                    and not self.falling
                    and not self.digging
                    and self.walking_left
                    else "0"
                ),
                "walk_right": (
                    "1"
                    if not self.splattered
                    and not self.falling
                    and not self.digging
                    and not self.walking_left
                    else "0"
                ),
                "aaah": "1" if not self.splattered and self.falling else "0",
                "digging": "1" if not self.splattered and self.digging else "0",
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
