import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer
            e = BinaryValue(stimulus["e"]).integer

            # Initialize output
            out = 0

            # Perform all 25 comparisons
            # out[24] = ~a ^ a
            out |= int(~(a ^ a) & 1) << 24
            # out[23] = ~a ^ b
            out |= int(~(a ^ b) & 1) << 23
            # out[22] = ~a ^ c
            out |= int(~(a ^ c) & 1) << 22
            # out[21] = ~a ^ d
            out |= int(~(a ^ d) & 1) << 21
            # out[20] = ~a ^ e
            out |= int(~(a ^ e) & 1) << 20

            # b comparisons
            out |= int(~(b ^ a) & 1) << 19
            out |= int(~(b ^ b) & 1) << 18
            out |= int(~(b ^ c) & 1) << 17
            out |= int(~(b ^ d) & 1) << 16
            out |= int(~(b ^ e) & 1) << 15

            # c comparisons
            out |= int(~(c ^ a) & 1) << 14
            out |= int(~(c ^ b) & 1) << 13
            out |= int(~(c ^ c) & 1) << 12
            out |= int(~(c ^ d) & 1) << 11
            out |= int(~(c ^ e) & 1) << 10

            # d comparisons
            out |= int(~(d ^ a) & 1) << 9
            out |= int(~(d ^ b) & 1) << 8
            out |= int(~(d ^ c) & 1) << 7
            out |= int(~(d ^ d) & 1) << 6
            out |= int(~(d ^ e) & 1) << 5

            # e comparisons
            out |= int(~(e ^ a) & 1) << 4
            out |= int(~(e ^ b) & 1) << 3
            out |= int(~(e ^ c) & 1) << 2
            out |= int(~(e ^ d) & 1) << 1
            out |= int(~(e ^ e) & 1) << 0

            # Convert to 25-bit binary string
            out_binary = BinaryValue(value=out, n_bits=25, bigEndian=True).binstr
            stimulus_outputs.append({"out": out_binary})

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
