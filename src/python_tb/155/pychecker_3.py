import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers:
        - walking_left: tracks if Lemming is walking left
        - falling: tracks if Lemming is falling
        """
        self.walking_left = True  # Start walking left
        self.falling = False

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process input stimuli and update Lemming state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Parse inputs
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])

            # Handle asynchronous reset
            if areset:
                self.walking_left = True
                self.falling = False
            else:
                # Update falling state
                self.falling = not ground

                # Update walking direction if not falling and bumped
                if not self.falling and (bump_left or bump_right):
                    self.walking_left = not self.walking_left

            # Generate outputs
            outputs = {
                "walk_left": "1" if self.walking_left and not self.falling else "0",
                "walk_right": (
                    "1" if not self.walking_left and not self.falling else "0"
                ),
                "aaah": "1" if self.falling else "0",
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
