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
            a = BinaryValue(stimulus["a"], n_bits=8)
            b = BinaryValue(stimulus["b"], n_bits=8)

            # Compute sum
            sum_val = (a.signed_integer + b.signed_integer) & 0xFF
            s = BinaryValue(value=sum_val, n_bits=8)

            # Check for overflow
            # Overflow occurs when:
            # 1. Both inputs positive (MSB=0) but sum is negative (MSB=1)
            # 2. Both inputs negative (MSB=1) but sum is positive (MSB=0)
            a_neg = (a.integer & 0x80) != 0
            b_neg = (b.integer & 0x80) != 0
            s_neg = (sum_val & 0x80) != 0

            overflow = (not a_neg and not b_neg and s_neg) or (
                a_neg and b_neg and not s_neg
            )

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
