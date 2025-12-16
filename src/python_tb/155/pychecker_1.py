import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Define states
        self.WALK_LEFT = 0
        self.WALK_RIGHT = 1
        self.FALL_LEFT = 2
        self.FALL_RIGHT = 3

        # Initialize state
        self.current_state = self.WALK_LEFT

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate types
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])

            # Handle asynchronous reset
            if areset:
                self.current_state = self.WALK_LEFT
            else:
                # State transition logic
                if ground == 0:  # Falling
                    if self.current_state == self.WALK_LEFT:
                        self.current_state = self.FALL_LEFT
                    elif self.current_state == self.WALK_RIGHT:
                        self.current_state = self.FALL_RIGHT
                else:  # Ground present
                    if self.current_state == self.FALL_LEFT:
                        self.current_state = self.WALK_LEFT
                    elif self.current_state == self.FALL_RIGHT:
                        self.current_state = self.WALK_RIGHT
                    else:  # Handle bumps only when not falling
                        if bump_left:
                            self.current_state = self.WALK_RIGHT
                        elif bump_right:
                            self.current_state = self.WALK_LEFT

            # Generate outputs based on current state
            walk_left = 1 if self.current_state in [self.WALK_LEFT] else 0
            walk_right = 1 if self.current_state in [self.WALK_RIGHT] else 0
            aaah = 1 if self.current_state in [self.FALL_LEFT, self.FALL_RIGHT] else 0

            # Create output dictionary for this stimulus
            output = {
                "walk_left": str(walk_left),
                "walk_right": str(walk_right),
                "aaah": str(aaah),
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
