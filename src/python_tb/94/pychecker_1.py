import json
from enum import Enum
from typing import Any, Dict, List, Union


class GoldenDUT:
    class State(Enum):
        SEARCH = 0
        BYTE2 = 1
        BYTE3 = 2

    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = self.State.SEARCH
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process input signals and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            reset = int(stimulus["reset"], 2)
            in_byte = int(stimulus["in"], 2)

            # Update state based on current inputs
            if reset:
                self.current_state = self.State.SEARCH
                self.done_reg = 0
            else:
                # Check bit 3 of input byte and current state
                if self.current_state == self.State.SEARCH:
                    if in_byte & 0x08:  # in[3] == 1
                        self.current_state = self.State.BYTE2
                        self.done_reg = 0
                    else:
                        self.done_reg = 0
                elif self.current_state == self.State.BYTE2:
                    self.current_state = self.State.BYTE3
                    self.done_reg = 0
                elif self.current_state == self.State.BYTE3:
                    self.current_state = self.State.SEARCH
                    self.done_reg = 1

            # Append current outputs to results
            stimulus_outputs.append({"done": format(self.done_reg, "b")})

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
