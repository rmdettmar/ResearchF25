import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 16-bit output register
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            resetn = BinaryValue(stimulus["resetn"]).integer
            byteena = BinaryValue(stimulus["byteena"]).integer
            d = BinaryValue(stimulus["d"]).integer

            if resetn == 0:
                # Synchronous reset
                self.q_reg = 0
            else:
                # Handle byte enables
                if byteena & 0b01:  # Lower byte enable
                    self.q_reg = (self.q_reg & 0xFF00) | (d & 0x00FF)
                if byteena & 0b10:  # Upper byte enable
                    self.q_reg = (self.q_reg & 0x00FF) | (d & 0xFF00)

            # Format output as 16-bit binary string
            q_bv = BinaryValue(value=self.q_reg, n_bits=16)
            stimulus_outputs.append({"q": q_bv.binstr})

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
