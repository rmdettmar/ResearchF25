import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize with no state variables since this is a combinational circuit"""
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and return constant 0 output"""
        # Create list of outputs for each stimulus
        stimulus_outputs = []

        # For each stimulus in the input
        for _ in stimulus_dict["input variable"]:
            # Create a BinaryValue object for output with value 0
            out_value = BinaryValue(value=0, n_bits=1)
            # Add the output dictionary to the list
            stimulus_outputs.append({"out": out_value.binstr})

        # Return the formatted output dictionary
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
