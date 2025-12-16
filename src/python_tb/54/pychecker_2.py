import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """No state variables needed for combinational logic"""
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process each input stimulus and generate corresponding output"""
        # Initialize output list
        stimulus_outputs = []

        # Process each stimulus
        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_val = BinaryValue(stimulus["in"])

            # Output follows input directly
            out_val = in_val.binstr

            # Add to output list
            stimulus_outputs.append({"out": out_val})

        # Return formatted output dictionary
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
