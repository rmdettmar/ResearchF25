import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])
            c_bv = BinaryValue(stimulus["c"])
            d_bv = BinaryValue(stimulus["d"])

            # Convert to boolean values
            a = a_bv.integer
            b = b_bv.integer
            c = c_bv.integer
            d = d_bv.integer

            # Implement K-map logic (setting don't cares to 0)
            # ab=00: out=1 when cd=11 or cd=10
            # ab=10/11: out=1 except when cd=01
            # ab=01: out=0 (don't care when cd=00 set to 0)
            if (
                (not a and not b and (c and not d or c and d))
                or ((a and not b) or (a and b))
                and not (not c and d)
            ):
                out = 1
            else:
                out = 0

            # Convert output to binary string
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
