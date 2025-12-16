import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal states:
        0: walking left
        1: walking right
        2: falling (was walking left)
        3: falling (was walking right)
        """
        self.current_state = 0  # Start walking left

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signals
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])

            # Handle asynchronous reset
            if areset:
                self.current_state = 0
            else:
                # State transitions
                if self.current_state == 0:  # Walking left
                    if not ground:
                        self.current_state = 2  # Fall while remembering left
                    elif bump_left:
                        self.current_state = 1  # Switch to walking right
                elif self.current_state == 1:  # Walking right
                    if not ground:
                        self.current_state = 3  # Fall while remembering right
                    elif bump_right:
                        self.current_state = 0  # Switch to walking left
                elif self.current_state == 2:  # Falling (was left)
                    if ground:
                        self.current_state = 0  # Resume walking left
                elif self.current_state == 3:  # Falling (was right)
                    if ground:
                        self.current_state = 1  # Resume walking right

            # Generate outputs based on current state
            walk_left = 1 if self.current_state == 0 else 0
            walk_right = 1 if self.current_state == 1 else 0
            aaah = 1 if self.current_state in [2, 3] else 0

            stimulus_outputs.append(
                {
                    "walk_left": str(walk_left),
                    "walk_right": str(walk_right),
                    "aaah": str(aaah),
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
