import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state registers needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to the wire connections
        """
        output_list = []

        # Process each stimulus in the input list
        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            a = BinaryValue(stimulus["a"], n_bits=1)
            b = BinaryValue(stimulus["b"], n_bits=1)
            c = BinaryValue(stimulus["c"], n_bits=1)

            # Create output dictionary for current stimulus
            output_dict = {
                "w": a.binstr,  # w = a
                "x": b.binstr,  # x = b
                "y": b.binstr,  # y = b
                "z": c.binstr,  # z = c
            }
            output_list.append(output_dict)

        # Return formatted output dictionary
        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
