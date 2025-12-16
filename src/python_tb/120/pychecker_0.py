import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 4-bit shift register state
        self.shift_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            resetn = BinaryValue(stimulus["resetn"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Handle reset condition
            if resetn == 0:
                self.shift_reg = 0
            else:
                # Shift left and input new bit
                self.shift_reg = ((self.shift_reg << 1) | in_bit) & 0xF

            # Output is the MSB (bit 3)
            out_bit = (self.shift_reg >> 3) & 1

            # Convert output to binary string format
            out_bv = BinaryValue(value=out_bit, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
