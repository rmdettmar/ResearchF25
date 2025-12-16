import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state storage needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            x = BinaryValue(stimulus["x"])

            # Extract individual bits
            x1 = (x.integer >> 0) & 1
            x2 = (x.integer >> 1) & 1
            x3 = (x.integer >> 2) & 1
            x4 = (x.integer >> 3) & 1

            # Implement the logic function based on Karnaugh map
            f = (
                (not x3 and not x4 and not x1 and not x2)
                or (not x3 and not x4 and x1 and not x2)
                or (x3 and x4 and not x1)
                or (x3 and x4 and not x2)
                or (x3 and not x4 and not x1)
                or (x3 and not x4 and not x2 and x1)
            )

            # Convert boolean to BinaryValue
            f_bin = BinaryValue(value=1 if f else 0, n_bits=1)
            stimulus_outputs.append({"f": f_bin.binstr})

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
