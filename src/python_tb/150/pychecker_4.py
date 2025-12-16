import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # State encoding
        self.WALK_LEFT = 0
        self.WALK_RIGHT = 1
        self.FALLING = 2
        self.DIGGING = 3
        self.SPLAT = 4

        # Initialize internal state
        self.current_state = self.WALK_LEFT
        self.fall_counter = 0
        self.last_direction = (
            self.WALK_LEFT
        )  # Remember direction before falling/digging

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            bump_left = BinaryValue(stimulus["bump_left"]).integer
            bump_right = BinaryValue(stimulus["bump_right"]).integer
            ground = BinaryValue(stimulus["ground"]).integer
            dig = BinaryValue(stimulus["dig"]).integer

            # Update state based on inputs
            if self.current_state != self.SPLAT:
                if not ground:
                    # Falling has highest priority
                    if self.current_state != self.FALLING:
                        self.last_direction = (
                            self.current_state
                            if self.current_state <= 1
                            else self.last_direction
                        )
                    self.current_state = self.FALLING
                    self.fall_counter += 1
                else:
                    # Ground present
                    if self.current_state == self.FALLING:
                        # Check for splatter
                        if self.fall_counter > 20:
                            self.current_state = self.SPLAT
                        else:
                            self.current_state = self.last_direction
                        self.fall_counter = 0
                    elif dig and self.current_state <= 1:
                        # Start digging if walking
                        self.last_direction = self.current_state
                        self.current_state = self.DIGGING
                    elif self.current_state <= 1:
                        # Handle direction changes while walking
                        if bump_left and not bump_right:
                            self.current_state = self.WALK_RIGHT
                        elif bump_right and not bump_left:
                            self.current_state = self.WALK_LEFT
                        elif bump_left and bump_right:
                            self.current_state = (
                                self.WALK_LEFT
                                if self.current_state == self.WALK_RIGHT
                                else self.WALK_RIGHT
                            )

            # Generate outputs based on current state
            walk_left = "1" if self.current_state == self.WALK_LEFT else "0"
            walk_right = "1" if self.current_state == self.WALK_RIGHT else "0"
            aaah = "1" if self.current_state == self.FALLING else "0"
            digging = "1" if self.current_state == self.DIGGING else "0"

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
