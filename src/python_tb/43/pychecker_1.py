import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 8-bit shift register with all zeros
        """
        self.shift_reg = 0  # 8-bit shift register Q[7:0]

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            enable = BinaryValue(stimulus["enable"]).integer
            S = BinaryValue(stimulus["S"]).integer
            A = BinaryValue(stimulus["A"]).integer
            B = BinaryValue(stimulus["B"]).integer
            C = BinaryValue(stimulus["C"]).integer

            # Update shift register if enable is high
            if enable:
                # Shift in new bit S (MSB first)
                self.shift_reg = ((self.shift_reg << 1) | S) & 0xFF

            # Calculate output Z based on ABC selection
            addr = (A << 2) | (B << 1) | C  # Combine ABC to form 3-bit address
            Z = (self.shift_reg >> addr) & 1  # Select appropriate bit

            # Format output as binary string
            Z_bin = BinaryValue(value=Z, n_bits=1)
            stimulus_outputs.append({"Z": Z_bin.binstr})

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
