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
            # Convert inputs to BinaryValue
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Implement K-map logic
            # Truth table implementation based on K-map
            out = (
                (not a and not b and not c and not d)  # 0000
                or (not a and not b and not c and d)  # 0001
                or (not a and not b and c and not d)  # 0010
                or (not a and b and c and d)  # 0111
                or (not a and b and not c and not d)  # 0100
                or (a and not b and not c and not d)  # 1000
                or (a and not b and not c and d)  # 1001
                or (a and b and c and d)  # 1111
                or (a and b and c and not d)  # 1110
            )

            # Convert boolean to BinaryValue
            out_bv = BinaryValue(value=1 if out else 0, n_bits=1)
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
