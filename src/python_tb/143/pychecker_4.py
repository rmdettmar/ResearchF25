import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            x_bv = BinaryValue(stimulus["x"])
            x = x_bv.integer

            # Extract individual bits
            x1 = (x >> 0) & 1  # x[1]
            x2 = (x >> 1) & 1  # x[2]
            x3 = (x >> 2) & 1  # x[3]
            x4 = (x >> 3) & 1  # x[4]

            # Implement K-map function
            f = (
                ((not x1) and (not x2) and (not x3) and (not x4))
                or ((not x1) and x2 and (not x3) and (not x4))
                or (x1 and (not x2) and x3 and x4)
                or (x1 and x2 and x3 and x4)
                or ((not x1) and (not x2) and x3 and (not x4))
                or ((not x1) and x2 and x3 and (not x4))
            )

            # Convert boolean to binary string
            f_str = "1" if f else "0"
            stimulus_outputs.append({"f": f_str})

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
