import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue
            a_bin = BinaryValue(stimulus["a"], n_bits=8)
            b_bin = BinaryValue(stimulus["b"], n_bits=8)

            # Get signed integer values
            a_int = a_bin.signed_integer
            b_int = b_bin.signed_integer

            # Perform addition
            s_int = (a_int + b_int) & 0xFF

            # Create sum BinaryValue
            s_bin = BinaryValue(value=s_int, n_bits=8)

            # Check for overflow
            # Overflow occurs when adding two numbers with the same sign
            # but getting a result with different sign
            a_sign = a_int >= 0
            b_sign = b_int >= 0
            s_sign = s_int >= 0

            overflow = (a_sign == b_sign) and (a_sign != s_sign)

            # Create output dictionary
            output_list.append(
                {"s": s_bin.binstr, "overflow": "1" if overflow else "0"}
            )

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
