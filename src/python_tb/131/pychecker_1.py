import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational half adder
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])

            # Calculate sum (XOR) and carry (AND)
            sum_val = (a_bv.integer ^ b_bv.integer) & 0x1
            cout_val = (a_bv.integer & b_bv.integer) & 0x1

            # Convert results to binary strings
            sum_bv = BinaryValue(value=sum_val, n_bits=1)
            cout_bv = BinaryValue(value=cout_val, n_bits=1)

            # Add output dictionary to results
            output = {"sum": sum_bv.binstr, "cout": cout_bv.binstr}
            stimulus_outputs.append(output)

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
