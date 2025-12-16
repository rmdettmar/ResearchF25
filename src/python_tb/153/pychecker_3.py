import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        WALK_LEFT = 0
        WALK_RIGHT = 1
        FALLING = 2
        DIGGING = 3

    def __init__(self):
        # Initialize state registers
        self.current_state = self.State.WALK_LEFT
        self.prev_direction = self.State.WALK_LEFT

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals
            areset = int(stimulus["areset"], 2)
            bump_left = int(stimulus["bump_left"], 2)
            bump_right = int(stimulus["bump_right"], 2)
            ground = int(stimulus["ground"], 2)
            dig = int(stimulus["dig"], 2)

            # Handle reset
            if areset:
                self.current_state = self.State.WALK_LEFT
                self.prev_direction = self.State.WALK_LEFT
            else:
                # State transitions
                if not ground:  # Falling has highest priority
                    if self.current_state != self.State.FALLING:
                        self.prev_direction = (
                            self.State.WALK_LEFT
                            if self.current_state == self.State.WALK_LEFT
                            else self.State.WALK_RIGHT
                        )
                    self.current_state = self.State.FALLING
                elif self.current_state == self.State.FALLING:
                    # Landing after fall
                    self.current_state = self.prev_direction
                elif (
                    dig
                    and ground
                    and self.current_state
                    not in [self.State.FALLING, self.State.DIGGING]
                ):
                    # Start digging
                    self.prev_direction = (
                        self.State.WALK_LEFT
                        if self.current_state == self.State.WALK_LEFT
                        else self.State.WALK_RIGHT
                    )
                    self.current_state = self.State.DIGGING
                elif self.current_state == self.State.DIGGING:
                    if not ground:  # Finished digging
                        self.current_state = self.State.FALLING
                else:
                    # Handle direction changes
                    if bump_left and not bump_right:
                        self.current_state = self.State.WALK_RIGHT
                    elif bump_right and not bump_left:
                        self.current_state = self.State.WALK_LEFT
                    elif bump_left and bump_right:
                        self.current_state = (
                            self.State.WALK_RIGHT
                            if self.current_state == self.State.WALK_LEFT
                            else self.State.WALK_LEFT
                        )

            # Generate outputs
            walk_left = "1" if self.current_state == self.State.WALK_LEFT else "0"
            walk_right = "1" if self.current_state == self.State.WALK_RIGHT else "0"
            aaah = "1" if self.current_state == self.State.FALLING else "0"
            digging = "1" if self.current_state == self.State.DIGGING else "0"

            stimulus_outputs.append(
                {
                    "walk_left": walk_left,
                    "walk_right": walk_right,
                    "aaah": aaah,
                    "digging": digging,
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
