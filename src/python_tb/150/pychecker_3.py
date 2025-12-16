import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.is_walking_left = True  # Start walking left
        self.is_falling = False
        self.is_digging = False
        self.is_splattered = False
        self.fall_counter = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to boolean/int
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])
            dig = int(stimulus["dig"])

            # Handle async reset
            if areset:
                self.is_walking_left = True
                self.is_falling = False
                self.is_digging = False
                self.is_splattered = False
                self.fall_counter = 0
            else:
                if not self.is_splattered:
                    # Check for falling condition (highest priority)
                    if not ground:
                        if not self.is_falling:
                            self.is_falling = True
                            self.is_digging = False
                        self.fall_counter += 1
                    elif self.is_falling:  # Landing
                        self.is_falling = False
                        if self.fall_counter > 20:
                            self.is_splattered = True
                        self.fall_counter = 0

                    # Handle digging (second priority)
                    if not self.is_falling and ground and dig and not self.is_digging:
                        self.is_digging = True
                    elif self.is_digging and not ground:
                        self.is_digging = False
                        self.is_falling = True

                    # Handle direction changes (lowest priority)
                    if not self.is_falling and not self.is_digging:
                        if bump_left:
                            self.is_walking_left = False
                        elif bump_right:
                            self.is_walking_left = True

            # Set outputs
            walk_left = (
                1
                if (
                    not self.is_splattered
                    and not self.is_falling
                    and not self.is_digging
                    and self.is_walking_left
                )
                else 0
            )
            walk_right = (
                1
                if (
                    not self.is_splattered
                    and not self.is_falling
                    and not self.is_digging
                    and not self.is_walking_left
                )
                else 0
            )
            aaah = 1 if (not self.is_splattered and self.is_falling) else 0
            digging = 1 if (not self.is_splattered and self.is_digging) else 0

            stimulus_outputs.append(
                {
                    "walk_left": str(walk_left),
                    "walk_right": str(walk_right),
                    "aaah": str(aaah),
                    "digging": str(digging),
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
