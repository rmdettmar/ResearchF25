import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            x_bv = BinaryValue(value=stimulus["x"], n_bits=4)
            x = x_bv.integer

            # Extract individual bits
            x1 = (x >> 0) & 1  # LSB
            x2 = (x >> 1) & 1
            x3 = (x >> 2) & 1
            x4 = (x >> 3) & 1  # MSB

            # Implement the logic function based on Karnaugh map
            # Choosing optimal values for don't-cares to simplify logic
            f = (
                1
                if (
                    (x3 and not x4)  # x3'x4=10
                    or (x3 and x4 and x1 and not x2)  # x3x4x1x2'=1110
                    or (x3 and x4 and x2 and not x1)  # x3x4x2x1'=1101
                )
                else 0
            )

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
