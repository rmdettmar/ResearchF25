import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_bv = BinaryValue(stimulus["in"], n_bits=4)
            in_val = in_bv.integer

            # Calculate out_both (3 bits)
            out_both = 0
            out_both |= ((in_val >> 2) & 1) & ((in_val >> 3) & 1)  # out_both[2]
            out_both |= (((in_val >> 1) & 1) & ((in_val >> 2) & 1)) << 1  # out_both[1]
            out_both |= ((in_val & 1) & ((in_val >> 1) & 1)) << 2  # out_both[0]
            out_both_bv = BinaryValue(value=out_both, n_bits=3)

            # Calculate out_any (3 bits)
            out_any = 0
            out_any |= ((in_val >> 3) & 1) | ((in_val >> 2) & 1)  # out_any[3]
            out_any |= (((in_val >> 2) & 1) | ((in_val >> 1) & 1)) << 1  # out_any[2]
            out_any |= (((in_val >> 1) & 1) | (in_val & 1)) << 2  # out_any[1]
            out_any_bv = BinaryValue(value=out_any, n_bits=3)

            # Calculate out_different (4 bits)
            out_different = 0
            out_different |= ((in_val >> 3) & 1) ^ (in_val & 1)  # out_different[3]
            out_different |= (
                ((in_val >> 2) & 1) ^ ((in_val >> 3) & 1)
            ) << 1  # out_different[2]
            out_different |= (
                ((in_val >> 1) & 1) ^ ((in_val >> 2) & 1)
            ) << 2  # out_different[1]
            out_different |= (
                (in_val & 1) ^ ((in_val >> 1) & 1)
            ) << 3  # out_different[0]
            out_different_bv = BinaryValue(value=out_different, n_bits=4)

            # Create output dictionary for this stimulus
            output = {
                "out_both": out_both_bv.binstr,
                "out_any": out_any_bv.binstr,
                "out_different": out_different_bv.binstr,
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
