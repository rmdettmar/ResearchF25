import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 4-bit shift register state
        """
        self.q_reg = BinaryValue(value=0, n_bits=4)

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimuli and update internal state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            shift_ena = int(stimulus["shift_ena"])
            count_ena = int(stimulus["count_ena"])
            data = int(stimulus["data"])

            current_q = self.q_reg.integer

            if shift_ena:
                # Shift operation: MSB first
                current_q = ((current_q << 1) & 0xE) | (data & 0x1)
            elif count_ena:
                # Down counter operation
                current_q = (current_q - 1) & 0xF

            # Update internal state
            self.q_reg = BinaryValue(value=current_q, n_bits=4)

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
