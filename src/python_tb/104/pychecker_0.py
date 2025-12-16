import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 16-bit register to 0
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state on each clock cycle
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            resetn = BinaryValue(stimulus["resetn"]).integer
            byteena = BinaryValue(stimulus["byteena"]).integer
            d = BinaryValue(stimulus["d"]).integer

            if resetn == 0:
                # Synchronous reset - clear all bits
                self.q_reg = 0
            else:
                # Current state
                new_q = self.q_reg

                # Update lower byte if byteena[0] is set
                if byteena & 0x1:
                    new_q = (new_q & 0xFF00) | (d & 0x00FF)

                # Update upper byte if byteena[1] is set
                if byteena & 0x2:
                    new_q = (new_q & 0x00FF) | (d & 0xFF00)

                self.q_reg = new_q

            # Convert output to 16-bit binary string
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
