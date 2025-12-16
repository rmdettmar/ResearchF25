import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize output registers
        self.left = 0
        self.down = 0
        self.right = 0
        self.up = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get the scancode from input
            scancode = int(stimulus["scancode"], 2)

            # Reset all outputs
            self.left = 0
            self.down = 0
            self.right = 0
            self.up = 0

            # Check scancode and set appropriate output
            if scancode == 0xE06B:
                self.left = 1
            elif scancode == 0xE072:
                self.down = 1
            elif scancode == 0xE074:
                self.right = 1
            elif scancode == 0xE075:
                self.up = 1

            # Append current outputs to results
            output_dict = {
                "left": format(self.left, "b"),
                "down": format(self.down, "b"),
                "right": format(self.right, "b"),
                "up": format(self.up, "b"),
            }
            stimulus_outputs.append(output_dict)

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
