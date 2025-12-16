import json
from enum import Enum
from typing import Any, Dict, List, Union


class GoldenDUT:
    class State(Enum):
        A = 0  # Reset/Idle state
        B1 = 1  # First w check
        B2 = 2  # Second w check
        B3 = 3  # Third w check

    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = self.State.A
        self.w_count = 0  # Counter for w=1 occurrences
        self.z_reg = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)
            s = int(stimulus["s"], 2)
            w = int(stimulus["w"], 2)

            # Handle reset
            if reset:
                self.current_state = self.State.A
                self.w_count = 0
                self.z_reg = 0
            else:
                # State machine transitions
                if self.current_state == self.State.A:
                    if s == 1:
                        self.current_state = self.State.B1
                        self.w_count = 1 if w == 1 else 0
                elif self.current_state == self.State.B1:
                    self.current_state = self.State.B2
                    self.w_count += 1 if w == 1 else 0
                elif self.current_state == self.State.B2:
                    self.current_state = self.State.B3
                    self.w_count += 1 if w == 1 else 0
                elif self.current_state == self.State.B3:
                    self.current_state = self.State.B1
                    # Set z based on previous 3 cycles
                    self.z_reg = 1 if self.w_count == 2 else 0
                    # Start counting new sequence
                    self.w_count = 1 if w == 1 else 0

            stimulus_outputs.append({"z": format(self.z_reg, "b")})

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
