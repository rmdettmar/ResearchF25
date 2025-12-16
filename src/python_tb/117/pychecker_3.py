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
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Implement K-map logic
            if c == 0 and d == 0:  # cd=00
                out = (
                    1
                    if (a == 0 and b == 0) or (a == 0 and b == 1) or (a == 1 and b == 0)
                    else 0
                )
            elif c == 0 and d == 1:  # cd=01
                out = 1 if (a == 0 and b == 0) or (a == 1 and b == 0) else 0
            elif c == 1 and d == 1:  # cd=11
                out = (
                    1
                    if (a == 0 and b == 1) or (a == 1 and b == 1) or (a == 1 and b == 0)
                    else 0
                )
            else:  # cd=10
                out = 1 if (a == 0 and b == 0) or (a == 0 and b == 1) else 0

            # Convert output to BinaryValue
            out_bv = BinaryValue(value=out, n_bits=1)
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
