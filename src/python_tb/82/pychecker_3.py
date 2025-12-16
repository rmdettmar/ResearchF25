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
            # Convert input binary string to BinaryValue
            x = BinaryValue(stimulus["x"])
            x_int = x.integer

            # Extract individual bits
            x1 = (x_int >> 0) & 1  # LSB
            x2 = (x_int >> 1) & 1
            x3 = (x_int >> 2) & 1
            x4 = (x_int >> 3) & 1  # MSB

            # Implement K-map logic
            # Choosing convenient values for don't-cares to simplify logic
            if ((x3 == 1 and x4 == 1) or (x3 == 1 and x4 == 0)) and (
                x1 == 0 and x2 == 0 or x1 == 0 and x2 == 1
            ):
                f = 1
            elif x3 == 0 and x4 == 1 and x1 == 1 and x2 == 1:
                f = 1
            else:
                f = 0

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
