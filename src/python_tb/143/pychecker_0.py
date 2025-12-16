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
            x = BinaryValue(stimulus["x"])

            # Extract individual bits
            x1 = x[0]  # x[1]
            x2 = x[1]  # x[2]
            x3 = x[2]  # x[3]
            x4 = x[3]  # x[4]

            # Implement K-map logic
            f = (
                (not x1 and not x2 and not x3 and not x4)
                or (x1 and not x2 and not x3 and not x4)
                or (not x1 and not x2 and x3 and not x4)
                or (x1 and not x2 and x3 and not x4)
                or (x1 and x2 and x3 and not x4)
                or (x1 and x2 and x3 and x4)
                or (x1 and not x2 and x3 and x4)
                or (x1 and x2 and not x3 and x4)
            )

            # Convert boolean to binary string
            f_bin = "1" if f else "0"
            stimulus_outputs.append({"f": f_bin})

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
