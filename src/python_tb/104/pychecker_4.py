import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 16-bit register to 0
        """
        self.q_reg = BinaryValue(value=0, n_bits=16)

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state based on byte enables
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            resetn = BinaryValue(stimulus["resetn"]).integer
            byteena = BinaryValue(stimulus["byteena"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Get current state
            q_current = self.q_reg.integer

            if resetn == 0:
                # Synchronous reset - clear all bits
                self.q_reg = BinaryValue(value=0, n_bits=16)
            else:
                # Handle byte enables
                new_q = q_current

                if byteena & 0b01:  # byteena[0] - lower byte
                    new_q = (new_q & 0xFF00) | (d & 0x00FF)

                if byteena & 0b10:  # byteena[1] - upper byte
                    new_q = (new_q & 0x00FF) | (d & 0xFF00)

                self.q_reg = BinaryValue(value=new_q, n_bits=16)

            # Add current output to results
            stimulus_outputs.append({"q": self.q_reg.binstr})

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
