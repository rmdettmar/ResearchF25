import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        pass  # No state needed as y is an input

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Calculate Y0 based on current state and input x
            Y0 = 0
            if y == 0 and x == 1:  # 000 -> 001
                Y0 = 1
            elif y == 1 and x == 0:  # 001 -> 001
                Y0 = 1
            elif y == 3 and x == 0:  # 011 -> 001
                Y0 = 1

            # Calculate output z
            z = 1 if y in [3, 4] else 0  # z=1 for states 011 and 100

            # Create output dictionary for this stimulus
            output = {"Y0": str(Y0), "z": str(z)}
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
