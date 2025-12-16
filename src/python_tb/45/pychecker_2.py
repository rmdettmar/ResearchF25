import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to boolean values
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Calculate out_sop using sum of products form
            # out_sop = (!a & !b & c & !d) | (!a & b & c & d) | (a & b & c & d)
            out_sop = (
                ((not a) and (not b) and c and (not d))
                or ((not a) and b and c and d)
                or (a and b and c and d)
            )

            # Calculate out_pos using product of sums form
            # Same logic but expressed differently
            out_pos = out_sop  # Both forms give same result

            # Convert boolean results back to binary strings
            result = {
                "out_sop": "1" if out_sop else "0",
                "out_pos": "1" if out_pos else "0",
            }
            stimulus_outputs.append(result)

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
