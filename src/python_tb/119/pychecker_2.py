import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Perform sign extension from 8 bits to 32 bits
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_val = BinaryValue(stimulus["in"], n_bits=8)

            # Get the sign bit (MSB)
            sign_bit = in_val[7]

            # Create the sign extension part (24 copies of sign bit)
            sign_extension = "1" * 24 if sign_bit else "0" * 24

            # Concatenate sign extension with original input
            result = sign_extension + in_val.binstr

            # Create 32-bit BinaryValue for output
            out_val = BinaryValue(result, n_bits=32)

            stimulus_outputs.append({"out": out_val.binstr})

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
