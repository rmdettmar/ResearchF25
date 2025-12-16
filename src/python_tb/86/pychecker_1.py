import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 4-bit shift register to 0
        """
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to shift/count enables
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate types
            shift_ena = int(BinaryValue(stimulus["shift_ena"]).value)
            count_ena = int(BinaryValue(stimulus["count_ena"]).value)
            data = int(BinaryValue(stimulus["data"]).value)

            # Update state based on control signals
            if shift_ena:
                # Shift operation: shift left and bring in new data at LSB
                self.q_reg = ((self.q_reg << 1) | data) & 0xF
            elif count_ena:
                # Count operation: decrement
                self.q_reg = (self.q_reg - 1) & 0xF

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
