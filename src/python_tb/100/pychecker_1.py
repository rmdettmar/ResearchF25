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
            # Get the input value and convert to BinaryValue
            in_val = BinaryValue(stimulus["in"], n_bits=8)

            # Calculate parity by XORing all bits
            # Count number of 1s in the input
            num_ones = in_val.binstr.count("1")

            # If number of 1s is odd, parity should be 1 to make total even
            parity = "1" if (num_ones % 2) == 1 else "0"

            # Create output dictionary for this stimulus
            output = {"parity": parity}
            stimulus_outputs.append(output)

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
