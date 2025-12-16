import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Reverse the bits of the 100-bit input vector
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get the input value and convert to BinaryValue
            in_val = BinaryValue(stimulus["in"], n_bits=100)

            # Reverse the bits by converting to string and reversing
            reversed_bits = in_val.binstr[::-1]

            # Convert back to BinaryValue to ensure proper formatting
            out_val = BinaryValue(reversed_bits, n_bits=100)

            # Create output dictionary for this stimulus
            output = {"out": out_val.binstr}
            stimulus_outputs.append(output)

        # Return the complete output dictionary
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
