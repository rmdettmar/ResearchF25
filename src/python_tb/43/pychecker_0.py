import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize 8-bit shift register Q
        """
        self.q_reg = 0  # 8-bit shift register

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to RTL specification
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            enable = BinaryValue(stimulus["enable"]).integer
            s_in = BinaryValue(stimulus["S"]).integer
            a = BinaryValue(stimulus["A"]).integer
            b = BinaryValue(stimulus["B"]).integer
            c = BinaryValue(stimulus["C"]).integer

            # Update shift register if enable is high
            if enable:
                # Shift left and insert new bit at LSB
                self.q_reg = ((self.q_reg << 1) | s_in) & 0xFF

            # Calculate output Z based on ABC selection
            selector = (a << 2) | (b << 1) | c
            z_out = (self.q_reg >> selector) & 1

            # Convert output to binary string format
            z_bin = BinaryValue(value=z_out, n_bits=1)

            # Add output to results
            stimulus_outputs.append({"Z": z_bin.binstr})

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
