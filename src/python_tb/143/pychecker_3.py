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
            # Get x input as BinaryValue
            x = BinaryValue(stimulus["x"], n_bits=4)

            # Extract individual bits
            x1 = (x.integer >> 0) & 1
            x2 = (x.integer >> 1) & 1
            x3 = (x.integer >> 2) & 1
            x4 = (x.integer >> 3) & 1

            # Implement K-map logic
            f = 0
            if x3 == 0 and x4 == 0:  # Row 00
                f = 1 if (x1 == 0 and x2 == 0) or (x1 == 0 and x2 == 1) else 0
            elif x3 == 1 and x4 == 1:  # Row 11
                f = 0 if (x1 == 0 and x2 == 1) else 1
            elif x3 == 1 and x4 == 0:  # Row 10
                f = 0 if (x1 == 1 and x2 == 1) else 1

            # Convert output to BinaryValue
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
