import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational circuit
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input scancode to integer
            scancode = BinaryValue(stimulus["scancode"]).integer

            # Initialize outputs
            outputs = {"left": "0", "down": "0", "right": "0", "up": "0"}

            # Check scancode and set appropriate output
            if scancode == 0xE06B:
                outputs["left"] = "1"
            elif scancode == 0xE072:
                outputs["down"] = "1"
            elif scancode == 0xE074:
                outputs["right"] = "1"
            elif scancode == 0xE075:
                outputs["up"] = "1"

            output_list.append(outputs)

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
