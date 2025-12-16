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
            # Convert input signals to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer
            e = BinaryValue(stimulus["e"]).integer

            # Calculate all 25 pairwise comparisons
            result = 0
            # Compare a with all inputs
            result |= int(not (a ^ a)) << 24
            result |= int(not (a ^ b)) << 23
            result |= int(not (a ^ c)) << 22
            result |= int(not (a ^ d)) << 21
            result |= int(not (a ^ e)) << 20
            # Compare b with all inputs
            result |= int(not (b ^ a)) << 19
            result |= int(not (b ^ b)) << 18
            result |= int(not (b ^ c)) << 17
            result |= int(not (b ^ d)) << 16
            result |= int(not (b ^ e)) << 15
            # Compare c with all inputs
            result |= int(not (c ^ a)) << 14
            result |= int(not (c ^ b)) << 13
            result |= int(not (c ^ c)) << 12
            result |= int(not (c ^ d)) << 11
            result |= int(not (c ^ e)) << 10
            # Compare d with all inputs
            result |= int(not (d ^ a)) << 9
            result |= int(not (d ^ b)) << 8
            result |= int(not (d ^ c)) << 7
            result |= int(not (d ^ d)) << 6
            result |= int(not (d ^ e)) << 5
            # Compare e with all inputs
            result |= int(not (e ^ a)) << 4
            result |= int(not (e ^ b)) << 3
            result |= int(not (e ^ c)) << 2
            result |= int(not (e ^ d)) << 1
            result |= int(not (e ^ e)) << 0

            # Convert result to 25-bit binary string
            out_bv = BinaryValue(value=result, n_bits=25, bigEndian=True)
            stimulus_outputs.append({"out": out_bv.binstr})

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
