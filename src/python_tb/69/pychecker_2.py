import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state variables"""
        self.Y0 = 0
        self.z = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Calculate outputs based on state table
            if y == 0b000:
                self.Y0 = 1 if x == 1 else 0
                self.z = 0
            elif y == 0b001:
                self.Y0 = 0 if x == 1 else 1
                self.z = 0
            elif y == 0b010:
                self.Y0 = 1 if x == 1 else 0
                self.z = 0
            elif y == 0b011:
                self.Y0 = 0 if x == 1 else 1
                self.z = 1
            elif y == 0b100:
                self.Y0 = 0 if x == 1 else 1
                self.z = 1

            # Add outputs to result list
            outputs.append({"Y0": format(self.Y0, "b"), "z": format(self.z, "b")})

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
