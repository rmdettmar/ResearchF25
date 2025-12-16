import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert scancode string to integer
            scancode = BinaryValue(stimulus["scancode"]).integer

            # Initialize all outputs to 0
            left = down = right = up = 0

            # Check scancode and set appropriate output
            if scancode == 0xE06B:
                left = 1
            elif scancode == 0xE072:
                down = 1
            elif scancode == 0xE074:
                right = 1
            elif scancode == 0xE075:
                up = 1

            # Add outputs to result list
            output_dict = {
                "left": str(left),
                "down": str(down),
                "right": str(right),
                "up": str(up),
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
