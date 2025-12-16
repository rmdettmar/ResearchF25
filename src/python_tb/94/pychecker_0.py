import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """Initialize state variables"""
        # FSM states
        self.SEARCH = 0
        self.BYTE2 = 1
        self.BYTE3 = 2

        # Internal state register
        self.current_state = self.SEARCH
        self.done_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """Process input signals and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings
            reset = int(stimulus["reset"], 2)
            in_byte = int(stimulus["in"], 2)

            # Update state based on inputs
            if reset:
                self.current_state = self.SEARCH
                self.done_reg = 0
            else:
                if self.current_state == self.SEARCH:
                    if in_byte & 0x08:  # Check in[3]=1
                        self.current_state = self.BYTE2
                        self.done_reg = 0
                    else:
                        self.done_reg = 0

                elif self.current_state == self.BYTE2:
                    self.current_state = self.BYTE3
                    self.done_reg = 0

                elif self.current_state == self.BYTE3:
                    self.current_state = self.SEARCH
                    self.done_reg = 1

            # Add output to results
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
