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
            # Convert input binary strings to BinaryValue objects
            a_bin = BinaryValue(stimulus["a"], n_bits=8)
            b_bin = BinaryValue(stimulus["b"], n_bits=8)

            # Get signed integer values
            a_val = a_bin.signed_integer
            b_val = b_bin.signed_integer

            # Calculate sum
            sum_val = a_val + b_val

            # Detect overflow
            overflow = False
            if (a_val >= 0 and b_val >= 0 and sum_val < 0) or (
                a_val < 0 and b_val < 0 and sum_val >= 0
            ):
                overflow = True

            # Wrap sum to 8 bits
            sum_val = sum_val & 0xFF

            # Convert sum back to binary string
            sum_bin = BinaryValue(value=sum_val, n_bits=8)

            # Create output dictionary for this stimulus
            output = {"s": sum_bin.binstr, "overflow": "1" if overflow else "0"}
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
