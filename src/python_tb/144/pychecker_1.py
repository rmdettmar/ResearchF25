import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state to 0 (equivalent to having seen a 0)
        self.state = 0  # Number of consecutive 1s seen
        self.disc = 0
        self.flag = 0
        self.err = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings to integers
            reset = int(stimulus["reset"], 2)
            in_bit = int(stimulus["in"], 2)

            # Update state based on reset and input
            if reset:
                self.state = 0
            else:
                if in_bit:
                    # Input is 1, increment consecutive 1s count
                    self.state += 1
                else:
                    # Input is 0, check for patterns and reset count
                    if self.state == 5:
                        # 0111110 pattern detected
                        self.disc = 1
                        self.flag = 0
                        self.err = 0
                    elif self.state == 6:
                        # 01111110 pattern detected
                        self.disc = 0
                        self.flag = 1
                        self.err = 0
                    else:
                        # No special pattern
                        self.disc = 0
                        self.flag = 0
                        self.err = 0
                    self.state = 0

                # Check for error condition (7 or more 1s)
                if self.state >= 7:
                    self.disc = 0
                    self.flag = 0
                    self.err = 1
                    self.state = 7  # Cap the state

            # Create output dictionary for current cycle
            output = {
                "disc": format(self.disc, "b"),
                "flag": format(self.flag, "b"),
                "err": format(self.err, "b"),
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
