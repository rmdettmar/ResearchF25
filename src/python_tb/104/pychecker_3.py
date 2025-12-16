import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 16-bit register q
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to byte enables
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to integers
            resetn = BinaryValue(stimulus["resetn"]).integer
            byteena = BinaryValue(stimulus["byteena"]).integer
            d = BinaryValue(stimulus["d"]).integer

            if resetn == 0:
                # Synchronous reset
                self.q_reg = 0
            else:
                # Create mask for selective byte updates
                mask = 0
                new_value = 0

                # Handle lower byte
                if byteena & 0x1:
                    mask |= 0xFF
                    new_value |= d & 0xFF

                # Handle upper byte
                if byteena & 0x2:
                    mask |= 0xFF00
                    new_value |= d & 0xFF00

                # Update only enabled bytes
                self.q_reg = (self.q_reg & ~mask) | (new_value & mask)

            # Convert output to 16-bit binary string
            q_bv = BinaryValue(value=self.q_reg, n_bits=16)
            stimulus_outputs.append({"q": q_bv.binstr})

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
