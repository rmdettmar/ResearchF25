import json
from enum import Enum
from typing import Any, Dict, List, Union


class GoldenDUT:
    class State(Enum):
        SEARCH = 0  # Looking for first byte
        COLLECT = 1  # Collecting remaining bytes

    def __init__(self):
        """
        Initialize state variables
        """
        self.current_state = self.State.SEARCH
        self.byte_count = 0
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimulus and generate output
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            in_byte = int(stimulus["in"], 2)
            reset = int(stimulus["reset"], 2)

            # Handle synchronous reset
            if reset:
                self.current_state = self.State.SEARCH
                self.byte_count = 0
                self.done_reg = 0
            else:
                # State machine logic
                if self.current_state == self.State.SEARCH:
                    # Check if this is first byte (in[3]=1)
                    if (in_byte & 0x08) != 0:  # Check bit 3
                        self.current_state = self.State.COLLECT
                        self.byte_count = 1
                        self.done_reg = 0
                    else:
                        self.done_reg = 0

                elif self.current_state == self.State.COLLECT:
                    self.byte_count += 1
                    if self.byte_count == 3:
                        self.current_state = self.State.SEARCH
                        self.byte_count = 0
                        self.done_reg = 1  # Signal done after third byte
                    else:
                        self.done_reg = 0

            # Append output to results
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
