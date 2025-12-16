import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []
        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            x = BinaryValue(stimulus["x"])

            # Extract individual bits
            x1 = x[0]  # x[1]
            x2 = x[1]  # x[2]
            x3 = x[2]  # x[3]
            x4 = x[3]  # x[4]

            # Implement logic based on Karnaugh map
            if x3 == 0 and x4 == 0:  # 00xx
                f = 0
            elif x3 == 0 and x4 == 1:  # 01xx
                f = 1 if (x1 == 1 and x2 == 1) else 0
            elif x3 == 1 and x4 == 1:  # 11xx
                f = 1 if (x1 == 0 or x2 == 0) else 0
            else:  # 10xx (x3 == 1 and x4 == 0)
                f = 1 if (x1 == 0 or x2 == 0) else 0

            # Convert output to binary string
            f_bv = BinaryValue(value=f, n_bits=1)
            stimulus_outputs.append({"f": f_bv.binstr})

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
