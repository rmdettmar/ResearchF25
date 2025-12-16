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
            # Convert input string to BinaryValue
            in_bv = BinaryValue(stimulus["in"])

            # Calculate AND of all bits
            out_and = 1
            for i in range(100):
                out_and &= in_bv[i].integer

            # Calculate OR of all bits
            out_or = 0
            for i in range(100):
                out_or |= in_bv[i].integer

            # Calculate XOR of all bits
            out_xor = 0
            for i in range(100):
                out_xor ^= in_bv[i].integer

            # Create output dictionary for this stimulus
            output = {
                "out_and": BinaryValue(value=out_and, n_bits=1).binstr,
                "out_or": BinaryValue(value=out_or, n_bits=1).binstr,
                "out_xor": BinaryValue(value=out_xor, n_bits=1).binstr,
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
