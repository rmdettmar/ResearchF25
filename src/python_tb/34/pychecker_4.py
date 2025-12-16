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
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])

            # Get integer values
            a_int = a.signed_integer
            b_int = b.signed_integer

            # Compute sum
            s_int = (a_int + b_int) & 0xFF

            # Detect overflow
            # Overflow occurs when:
            # 1. Both inputs positive but sum is negative
            # 2. Both inputs negative but sum is positive
            overflow = False
            if (a_int >= 0 and b_int >= 0 and s_int < 0) or (
                a_int < 0 and b_int < 0 and s_int >= 0
            ):
                overflow = True

            # Convert sum to 8-bit BinaryValue
            s = BinaryValue(value=s_int, n_bits=8)

            # Create output dictionary
            output = {"s": s.binstr, "overflow": "1" if overflow else "0"}
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
