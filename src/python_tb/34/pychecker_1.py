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
            # Convert input binary strings to BinaryValue
            a_bin = BinaryValue(stimulus["a"], n_bits=8)
            b_bin = BinaryValue(stimulus["b"], n_bits=8)

            # Get signed integer values
            a_val = a_bin.signed_integer
            b_val = b_bin.signed_integer

            # Perform addition
            s_val = (a_val + b_val) & 0xFF

            # Convert sum to BinaryValue for output
            s_bin = BinaryValue(value=s_val, n_bits=8)

            # Detect overflow:
            # If both inputs are positive and sum is negative, or
            # both inputs are negative and sum is positive
            a_pos = a_val >= 0
            b_pos = b_val >= 0
            s_pos = (s_val & 0x80) == 0

            overflow = (a_pos and b_pos and not s_pos) or (
                not a_pos and not b_pos and s_pos
            )

            # Create output dictionary
            output = {"s": s_bin.binstr, "overflow": "1" if overflow else "0"}
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
