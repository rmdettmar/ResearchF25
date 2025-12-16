import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 16-bit register to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue objects
            resetn = BinaryValue(stimulus["resetn"]).integer
            byteena = BinaryValue(stimulus["byteena"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Handle reset condition
            if not resetn:
                self.q_reg = 0
            else:
                # Get current value
                current_q = self.q_reg

                # Handle byte enables
                if byteena & 0b01:  # Lower byte enable
                    current_q = (current_q & 0xFF00) | (d & 0x00FF)
                if byteena & 0b10:  # Upper byte enable
                    current_q = (current_q & 0x00FF) | (d & 0xFF00)

                self.q_reg = current_q

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
