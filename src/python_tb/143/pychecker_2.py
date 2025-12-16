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
            x = BinaryValue(stimulus["x"])

            # Extract x[4:1] bits
            x1 = (x.integer >> 0) & 1  # x[1]
            x2 = (x.integer >> 1) & 1  # x[2]
            x3 = (x.integer >> 2) & 1  # x[3]
            x4 = (x.integer >> 3) & 1  # x[4]

            # Evaluate function f based on K-map conditions
            f = 0
            if (x3 == 0 and x4 == 0) and (x1 == 0 and x2 == 0 or x1 == 0 and x2 == 1):
                f = 1
            elif (x3 == 1 and x4 == 0) and (x1 == 0 or x1 == 1 and x2 == 0):
                f = 1
            elif (x3 == 1 and x4 == 1) and (
                x1 == 0 or x1 == 1 and x2 == 0 or x1 == 1 and x2 == 1
            ):
                f = 1

            # Convert output to binary string
            f_bv = BinaryValue(value=f, n_bits=1)
            stimulus_outputs.append({"f": f_bv.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
