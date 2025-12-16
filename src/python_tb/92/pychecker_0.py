import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables
        States: A=0, B=1, C=2, D=3
        """
        self.current_state = 0  # Initialize to state A
        self.g = 0  # Initialize grants to 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            resetn = int(stimulus["resetn"], 2)
            r = int(stimulus["r"], 2)

            # Extract individual request bits
            r1 = (r >> 0) & 1  # r[1]
            r2 = (r >> 1) & 1  # r[2]
            r3 = (r >> 2) & 1  # r[3]

            # State transition logic
            if resetn == 0:
                self.current_state = 0  # Reset to state A
            else:
                if self.current_state == 0:  # State A
                    if r1:
                        self.current_state = 1  # Go to state B
                    elif r2:
                        self.current_state = 2  # Go to state C
                    elif r3:
                        self.current_state = 3  # Go to state D
                elif self.current_state == 1:  # State B
                    if not r1:
                        self.current_state = 0  # Return to A if r1 deasserted
                elif self.current_state == 2:  # State C
                    if not r2:
                        self.current_state = 0  # Return to A if r2 deasserted
                elif self.current_state == 3:  # State D
                    if not r3:
                        self.current_state = 0  # Return to A if r3 deasserted

            # Output logic
            if self.current_state == 1:  # State B
                self.g = 0b001  # g[1] = 1
            elif self.current_state == 2:  # State C
                self.g = 0b010  # g[2] = 1
            elif self.current_state == 3:  # State D
                self.g = 0b100  # g[3] = 1
            else:  # State A
                self.g = 0b000  # All grants 0

            # Format output as binary string
            g_str = format(self.g, "03b")
            stimulus_outputs.append({"g": g_str})

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
