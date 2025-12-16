import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Create mapping dictionary for valid codes
        self.code_map = {
            0x45: 0,
            0x16: 1,
            0x1E: 2,
            0x26: 3,
            0x25: 4,
            0x2E: 5,
            0x36: 6,
            0x3D: 7,
            0x3E: 8,
            0x46: 9,
        }

    def load(self, stimulus_dict: Dict[str, any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input code string to BinaryValue
            code_bv = BinaryValue(stimulus["code"])
            code_int = code_bv.integer

            # Check if code is in our mapping
            if code_int in self.code_map:
                out = self.code_map[code_int]
                valid = 1
            else:
                out = 0
                valid = 0

            # Convert outputs to binary strings
            out_bv = BinaryValue(value=out, n_bits=4)
            valid_bv = BinaryValue(value=valid, n_bits=1)

            # Add to output list
            output_list.append({"out": out_bv.binstr, "valid": valid_bv.binstr})

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
