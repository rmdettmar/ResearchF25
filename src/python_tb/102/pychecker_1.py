import json
from typing import Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize the model"""
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            x_bv = BinaryValue(stimulus["x"])
            y_bv = BinaryValue(stimulus["y"])

            # Convert to integers for logical operations
            x = x_bv.integer
            y = y_bv.integer

            # Implement XNOR logic
            z = int(not (x ^ y))

            # Convert result to BinaryValue and then to binary string
            z_bv = BinaryValue(value=z, n_bits=1)

            # Add to output list
            stimulus_outputs.append({"z": z_bv.binstr})

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
