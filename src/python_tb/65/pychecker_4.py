import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def _xnor_compare(self, a: int, b: int) -> int:
        # Return 1 if bits are equal, 0 if different
        return 1 if a == b else 0

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer
            e = BinaryValue(stimulus["e"]).integer

            # Calculate all 25 comparisons
            out = 0
            # Compare a with all inputs
            out |= self._xnor_compare(a, a) << 24
            out |= self._xnor_compare(a, b) << 23
            out |= self._xnor_compare(a, c) << 22
            out |= self._xnor_compare(a, d) << 21
            out |= self._xnor_compare(a, e) << 20
            # Compare b with all inputs
            out |= self._xnor_compare(b, a) << 19
            out |= self._xnor_compare(b, b) << 18
            out |= self._xnor_compare(b, c) << 17
            out |= self._xnor_compare(b, d) << 16
            out |= self._xnor_compare(b, e) << 15
            # Compare c with all inputs
            out |= self._xnor_compare(c, a) << 14
            out |= self._xnor_compare(c, b) << 13
            out |= self._xnor_compare(c, c) << 12
            out |= self._xnor_compare(c, d) << 11
            out |= self._xnor_compare(c, e) << 10
            # Compare d with all inputs
            out |= self._xnor_compare(d, a) << 9
            out |= self._xnor_compare(d, b) << 8
            out |= self._xnor_compare(d, c) << 7
            out |= self._xnor_compare(d, d) << 6
            out |= self._xnor_compare(d, e) << 5
            # Compare e with all inputs
            out |= self._xnor_compare(e, a) << 4
            out |= self._xnor_compare(e, b) << 3
            out |= self._xnor_compare(e, c) << 2
            out |= self._xnor_compare(e, d) << 1
            out |= self._xnor_compare(e, e)

            # Convert to 25-bit binary string
            out_bin = format(out, "025b")
            stimulus_outputs.append({"out": out_bin})

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
