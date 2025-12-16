import json
from enum import Enum
from typing import Any, Dict, List, Union


class GoldenDUT:
    class State(Enum):
        SEARCH = 0  # Looking for first byte
        BYTE2 = 1  # Receiving second byte
        BYTE3 = 2  # Receiving third byte

    def __init__(self):
        """
        Initialize FSM state
        """
        self.current_state = self.State.SEARCH
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input signals and update FSM state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            reset = int(stimulus["reset"], 2)
            in_byte = int(stimulus["in"], 2)

            # Update state and outputs
            if reset:
                self.current_state = self.State.SEARCH
                self.done_reg = 0
            else:
                # FSM state transitions
                if self.current_state == self.State.SEARCH:
                    if (in_byte & 0x08) != 0:  # Check if in[3] = 1
                        self.current_state = self.State.BYTE2
                    self.done_reg = 0
                elif self.current_state == self.State.BYTE2:
                    self.current_state = self.State.BYTE3
                    self.done_reg = 0
                elif self.current_state == self.State.BYTE3:
                    self.current_state = self.State.SEARCH
                    self.done_reg = 1

            # Append output to stimulus_outputs
            stimulus_outputs.append({"done": format(self.done_reg, "b")})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
