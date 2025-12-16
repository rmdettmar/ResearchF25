import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 4-bit register q
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimuli and generate outputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary string inputs to values
            shift_ena = BinaryValue(stimulus["shift_ena"]).integer
            count_ena = BinaryValue(stimulus["count_ena"]).integer
            data = BinaryValue(stimulus["data"]).integer

            # Process according to control signals
            if shift_ena:
                # Shift operation: shift in data from MSB
                self.q_reg = ((self.q_reg << 1) | data) & 0xF
            elif count_ena:
                # Count operation: decrement
                self.q_reg = (self.q_reg - 1) & 0xF

            # Convert output to binary string format
            q_bv = BinaryValue(value=self.q_reg, n_bits=4)
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
