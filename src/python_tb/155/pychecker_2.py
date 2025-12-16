import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State definitions
        self.WALK_LEFT = 0
        self.WALK_RIGHT = 1

        # Initialize state registers
        self.walking_state = self.WALK_LEFT  # Current walking direction
        self.falling_state = False  # Whether Lemming is falling
        self.prev_direction = self.WALK_LEFT  # Direction before falling

    def load(self, stimulus_dict: Dict[str, Any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate types
            areset = int(stimulus["areset"])
            bump_left = int(stimulus["bump_left"])
            bump_right = int(stimulus["bump_right"])
            ground = int(stimulus["ground"])

            # Handle asynchronous reset
            if areset:
                self.walking_state = self.WALK_LEFT
                self.falling_state = False
                self.prev_direction = self.WALK_LEFT
            else:
                # Check ground state first
                if not ground:
                    if not self.falling_state:
                        # Just started falling, save direction
                        self.prev_direction = self.walking_state
                    self.falling_state = True
                else:
                    if self.falling_state:
                        # Just landed, restore direction
                        self.walking_state = self.prev_direction
                    self.falling_state = False

                    # Handle direction changes only when not falling
                    if not self.falling_state:
                        if bump_left and not bump_right:
                            self.walking_state = self.WALK_RIGHT
                        elif bump_right and not bump_left:
                            self.walking_state = self.WALK_LEFT
                        elif bump_left and bump_right:
                            # Switch direction when bumped on both sides
                            self.walking_state = (
                                self.WALK_RIGHT
                                if self.walking_state == self.WALK_LEFT
                                else self.WALK_LEFT
                            )

            # Prepare outputs
            walk_left = (
                "1"
                if self.walking_state == self.WALK_LEFT and not self.falling_state
                else "0"
            )
            walk_right = (
                "1"
                if self.walking_state == self.WALK_RIGHT and not self.falling_state
                else "0"
            )
            aaah = "1" if self.falling_state else "0"

            outputs.append(
                {"walk_left": walk_left, "walk_right": walk_right, "aaah": aaah}
            )

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
