import json
from typing import Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Compute intermediate results (AND gates)
            and1_out = a & b
            and2_out = c & d

            # Compute OR gate output
            out = and1_out | and2_out

            # Compute inverted output
            out_n = not out

            # Convert to binary strings
            out_bv = BinaryValue(value=out, n_bits=1)
            out_n_bv = BinaryValue(value=out_n, n_bits=1)

            # Add to output list
            stimulus_outputs.append({"out": out_bv.binstr, "out_n": out_n_bv.binstr})

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
