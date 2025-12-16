import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])

            # Get integer values
            a = a_bv.integer
            b = b_bv.integer

            # Compute all logic operations
            out_and = a & b
            out_or = a | b
            out_xor = a ^ b
            out_nand = ~(a & b) & 1  # Ensure single bit
            out_nor = ~(a | b) & 1
            out_xnor = ~(a ^ b) & 1
            out_anotb = a & (~b & 1)

            # Create output dictionary for this stimulus
            output = {
                "out_and": BinaryValue(value=out_and, n_bits=1).binstr,
                "out_or": BinaryValue(value=out_or, n_bits=1).binstr,
                "out_xor": BinaryValue(value=out_xor, n_bits=1).binstr,
                "out_nand": BinaryValue(value=out_nand, n_bits=1).binstr,
                "out_nor": BinaryValue(value=out_nor, n_bits=1).binstr,
                "out_xnor": BinaryValue(value=out_xnor, n_bits=1).binstr,
                "out_anotb": BinaryValue(value=out_anotb, n_bits=1).binstr,
            }

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
