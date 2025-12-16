import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


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
            # Convert scancode input string to BinaryValue
            scancode_str = stimulus["scancode"]
            scancode_bv = BinaryValue(scancode_str)
            scancode = scancode_bv.integer

            # Reset all outputs
            self.left = 0
            self.down = 0
            self.right = 0
            self.up = 0

            # Check scancode and set appropriate output
            if scancode == 0xE06B:  # left arrow
                self.left = 1
            elif scancode == 0xE072:  # down arrow
                self.down = 1
            elif scancode == 0xE074:  # right arrow
                self.right = 1
            elif scancode == 0xE075:  # up arrow
                self.up = 1

            # Create output dictionary for current stimulus
            output = {
                "left": BinaryValue(self.left, n_bits=1).binstr,
                "down": BinaryValue(self.down, n_bits=1).binstr,
                "right": BinaryValue(self.right, n_bits=1).binstr,
                "up": BinaryValue(self.up, n_bits=1).binstr,
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
