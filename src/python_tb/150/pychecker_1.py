import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.walking_left = True  # Initial direction is left
        self.fall_counter = 0
        self.is_splattered = False
        self.prev_direction = True  # Store direction before falling
        self.is_digging = False

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Don't process if splattered
            if self.is_splattered:
                stimulus_outputs.append(
                    {"walk_left": "0", "walk_right": "0", "aaah": "0", "digging": "0"}
                )
                continue

            # Get input signals
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])
            dig = int(stimulus["dig"])

            # Check for falling
            if ground == 0:
                # Start/continue falling
                self.fall_counter += 1
                self.is_digging = False
                stimulus_outputs.append(
                    {"walk_left": "0", "walk_right": "0", "aaah": "1", "digging": "0"}
                )
                continue

            # Check for splatter when hitting ground
            if self.fall_counter > 20 and ground == 1:
                self.is_splattered = True
                stimulus_outputs.append(
                    {"walk_left": "0", "walk_right": "0", "aaah": "0", "digging": "0"}
                )
                continue

            # Reset fall counter when on ground
            if ground == 1:
                self.fall_counter = 0

            # Check for digging
            if dig == 1 and ground == 1 and not self.is_digging:
                self.is_digging = True

            # Process direction changes if not digging
            if not self.is_digging:
                if bump_left and not bump_right:
                    self.walking_left = False
                elif bump_right and not bump_left:
                    self.walking_left = True
                elif bump_left and bump_right:
                    self.walking_left = not self.walking_left

            # Generate outputs
            stimulus_outputs.append(
                {
                    "walk_left": (
                        "1" if self.walking_left and not self.is_digging else "0"
                    ),
                    "walk_right": (
                        "1" if not self.walking_left and not self.is_digging else "0"
                    ),
                    "aaah": "0",
                    "digging": "1" if self.is_digging else "0",
                }
            )

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
