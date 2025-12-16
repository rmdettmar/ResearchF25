import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this simple circuit
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Returns a dictionary with the 'one' output always set to logic high
        """
        stimulus_outputs = []
        for _ in stimulus_dict["input variable"]:
            # Create a 1-bit BinaryValue with value 1
            one_value = BinaryValue(value=1, n_bits=1)
            stimulus_outputs.append({"one": one_value.binstr})

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
