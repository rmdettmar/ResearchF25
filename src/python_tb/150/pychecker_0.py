import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.walking_left = True  # Start walking left
        self.falling = False
        self.is_digging = False
        self.splattered = False
        self.fall_counter = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Handle reset first
            if "areset" in stimulus and stimulus["areset"] == "1":
                self.walking_left = True
                self.falling = False
                self.is_digging = False
                self.splattered = False
                self.fall_counter = 0
            else:
                # Parse inputs
                ground = stimulus["ground"] == "1"
                bump_left = stimulus["bump_left"] == "1"
                bump_right = stimulus["bump_right"] == "1"
                dig = stimulus["dig"] == "1"

                if not self.splattered:
                    # Handle falling
                    if not ground:
                        if not self.falling:
                            self.falling = True
                            self.is_digging = False
                        self.fall_counter += 1
                    elif self.falling:  # Landing
                        if self.fall_counter > 20:
                            self.splattered = True
                        self.falling = False
                        self.fall_counter = 0

                    # Handle digging
                    if not self.falling and ground and dig and not self.is_digging:
                        self.is_digging = True

                    # Handle direction changes
                    if not self.falling and not self.is_digging:
                        if bump_left:
                            self.walking_left = False
                        elif bump_right:
                            self.walking_left = True

            # Set outputs
            outputs = {}
            if self.splattered:
                outputs["walk_left"] = "0"
                outputs["walk_right"] = "0"
                outputs["aaah"] = "0"
                outputs["digging"] = "0"
            else:
                outputs["walk_left"] = (
                    "1"
                    if self.walking_left and not self.falling and not self.is_digging
                    else "0"
                )
                outputs["walk_right"] = (
                    "1"
                    if not self.walking_left
                    and not self.falling
                    and not self.is_digging
                    else "0"
                )
                outputs["aaah"] = "1" if self.falling else "0"
                outputs["digging"] = "1" if self.is_digging else "0"

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
