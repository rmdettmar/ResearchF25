import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input x to BinaryValue and extract bits
            x_bv = BinaryValue(stimulus["x"])
            x1 = x_bv[0]  # x[1]
            x2 = x_bv[1]  # x[2]
            x3 = x_bv[2]  # x[3]
            x4 = x_bv[3]  # x[4]

            # Implement logic function based on Karnaugh map
            x34 = x3 * 2 + x4  # Combine x3,x4
            x12 = x1 * 2 + x2  # Combine x1,x2

            # Check conditions for f=1
            f = 0
            if (
                (x34 == 3 and (x12 == 0 or x12 == 1))
                or (x34 == 2 and (x12 == 0 or x12 == 1))
                or (x34 == 1 and x12 == 3)
            ):
                f = 1

            stimulus_outputs.append({"f": str(f)})

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
