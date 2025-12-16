import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state initialization needed for this simple combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Returns a dictionary with the output signal 'out' always set to 0
        """
        # Create output value using BinaryValue
        out_value = BinaryValue(value=0, n_bits=1)

        # Create list of output dictionaries for each stimulus
        output_values = [
            {"out": out_value.binstr} for _ in stimulus_dict["input variable"]
        ]

        # Format the output dictionary
        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": output_values,
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
