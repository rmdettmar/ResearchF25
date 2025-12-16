import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this simple module
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        # Create a list of outputs, one for each input stimulus
        stimulus_outputs = []

        # For each input stimulus, output will always be 0
        for _ in stimulus_dict["input variable"]:
            # Create output dictionary with 'out' always set to 0
            out_val = BinaryValue(value=0, n_bits=1)
            stimulus_outputs.append({"out": out_val.binstr})

        # Return the output dictionary in the required format
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
