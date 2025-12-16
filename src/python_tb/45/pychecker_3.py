import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # This is combinational logic, no state needed
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to integers
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Calculate input number
            input_num = (a << 3) | (b << 2) | (c << 1) | d

            # Sum of Products implementation
            # out_sop = (2,7,15)
            out_sop = (
                (not a and not b and c and not d)  # 2
                or (not a and b and c and d)  # 7
                or (a and b and c and d)
            )  # 15

            # Product of Sums implementation
            # out_pos = (0,1,4,5,6,9,10,13,14)
            out_pos = (
                (a or b or c or d)  # not 0
                and (a or b or c or not d)  # not 1
                and (a or not b or c or d)  # not 4
                and (a or not b or c or not d)  # not 5
                and (a or not b or not c or not d)  # not 6
                and (not a or b or c or d)  # not 9
                and (not a or b or c or not d)  # not 10
                and (not a or not b or c or d)  # not 13
                and (not a or not b or c or not d)
            )  # not 14

            # Convert boolean results to binary strings
            out_sop_bin = BinaryValue(value=int(out_sop), n_bits=1).binstr
            out_pos_bin = BinaryValue(value=int(out_pos), n_bits=1).binstr

            stimulus_outputs.append({"out_sop": out_sop_bin, "out_pos": out_pos_bin})

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
