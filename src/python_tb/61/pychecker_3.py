import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for a NOT gate
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        # Process each input stimulus and generate corresponding output
        output_values = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            input_val = BinaryValue(stimulus["in"])

            # Perform NOT operation
            output_val = "1" if input_val.integer == 0 else "0"

            # Add to output list
            output_values.append({"out": output_val})

        # Return results in required format
        return {"scenario": stimulus_dict["scenario"], "output variable": output_values}


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
