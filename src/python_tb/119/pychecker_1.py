import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Implements 8-bit to 32-bit sign extension
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_bv = BinaryValue(stimulus["in"], n_bits=8)

            # Get the sign bit (MSB)
            sign_bit = in_bv[7]

            # Create the sign extension part (24 copies of sign bit)
            if sign_bit == "1":
                extension = "1" * 24
            else:
                extension = "0" * 24

            # Concatenate the extension with original input
            out_str = extension + in_bv.binstr

            # Convert to 32-bit BinaryValue
            out_bv = BinaryValue(out_str, n_bits=32)

            # Add to output list
            stimulus_outputs.append({"out": out_bv.binstr})

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
