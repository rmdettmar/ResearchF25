import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Half adder has no internal state to initialize
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Implements half adder logic:
        sum = a XOR b
        cout = a AND b
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])

            # Convert to integers for calculation
            a = a_bv.integer
            b = b_bv.integer

            # Calculate sum and carry
            sum_out = a ^ b  # XOR operation
            cout = a & b  # AND operation

            # Convert outputs to BinaryValue and then to binary strings
            sum_bv = BinaryValue(value=sum_out, n_bits=1)
            cout_bv = BinaryValue(value=cout, n_bits=1)

            # Create output dictionary for this stimulus
            output = {"sum": sum_bv.binstr, "cout": cout_bv.binstr}
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
