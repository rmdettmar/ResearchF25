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
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"], n_bits=3)
            b_bv = BinaryValue(stimulus["b"], n_bits=3)

            # Compute bitwise OR
            out_or_bitwise = a_bv.integer | b_bv.integer
            out_or_bitwise_bv = BinaryValue(value=out_or_bitwise, n_bits=3)

            # Compute logical OR
            out_or_logical = 1 if (a_bv.integer or b_bv.integer) else 0
            out_or_logical_bv = BinaryValue(value=out_or_logical, n_bits=1)

            # Compute NOT operations
            not_a = (~a_bv.integer) & 0x7  # Mask to 3 bits
            not_b = (~b_bv.integer) & 0x7  # Mask to 3 bits

            # Combine NOT results
            out_not = (not_b << 3) | not_a
            out_not_bv = BinaryValue(value=out_not, n_bits=6)

            # Create output dictionary for this stimulus
            output = {
                "out_or_bitwise": out_or_bitwise_bv.binstr,
                "out_or_logical": out_or_logical_bv.binstr,
                "out_not": out_not_bv.binstr,
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
