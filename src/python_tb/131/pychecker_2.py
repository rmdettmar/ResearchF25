import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for combinational circuit
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])

            # Convert to integers for computation
            a = a_bv.integer
            b = b_bv.integer

            # Compute sum and carry
            sum_out = a ^ b  # XOR for sum
            cout = a & b  # AND for carry

            # Convert outputs back to binary strings
            sum_bv = BinaryValue(value=sum_out, n_bits=1)
            cout_bv = BinaryValue(value=cout, n_bits=1)

            # Add outputs to result list
            stimulus_outputs.append({"sum": sum_bv.binstr, "cout": cout_bv.binstr})

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
