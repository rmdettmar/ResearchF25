import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            x_bv = BinaryValue(stimulus["x"])
            y_bv = BinaryValue(stimulus["y"])

            # Get integer values
            x = x_bv.integer
            y = y_bv.integer

            # Implement logic: z = (NOT x AND NOT y) OR (x AND y)
            z = (not x and not y) or (x and y)

            # Convert result to BinaryValue and then to string
            z_bv = BinaryValue(value=int(z), n_bits=1)

            # Add to outputs
            stimulus_outputs.append({"z": z_bv.binstr})

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
