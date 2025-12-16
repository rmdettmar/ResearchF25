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
            in_bv = BinaryValue(stimulus["in"], n_bits=8)

            # Get the sign bit (MSB)
            sign_bit = in_bv[7]

            # Create the sign-extended value
            # If sign_bit is 1, upper bits should be all 1s (0xFFFFFF)
            # If sign_bit is 0, upper bits should be all 0s (0x000000)
            upper_bits = 0xFFFFFF if sign_bit else 0x000000

            # Combine upper bits with original input
            out_value = (upper_bits << 8) | in_bv.integer

            # Convert to 32-bit BinaryValue
            out_bv = BinaryValue(value=out_value, n_bits=32)

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
