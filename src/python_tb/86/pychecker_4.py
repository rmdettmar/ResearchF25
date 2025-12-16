import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 4-bit shift register to 0
        """
        self.q_reg = 0  # 4-bit register

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to shift/count enables
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            shift_ena = BinaryValue(stimulus["shift_ena"]).integer
            count_ena = BinaryValue(stimulus["count_ena"]).integer
            data = BinaryValue(stimulus["data"]).integer

            # Current state
            current_q = self.q_reg

            if shift_ena:
                # Shift operation: shift right, new data into MSB
                self.q_reg = ((current_q >> 1) | (data << 3)) & 0xF
            elif count_ena:
                # Count down operation
                self.q_reg = (current_q - 1) & 0xF

            # Format output as 4-bit binary string
            out_q = BinaryValue(value=self.q_reg, n_bits=4)
            stimulus_outputs.append({"q": out_q.binstr})

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
