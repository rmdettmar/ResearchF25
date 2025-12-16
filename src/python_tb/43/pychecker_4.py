import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 8-bit shift register Q[7:0]
        self.q_reg = [0] * 8
        self.z_out = 0

    def load(self, stimulus_dict: Dict[str, Any]):
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
                # Shift values right (Q[7] to Q[0])
                for i in range(7, 0, -1):
                    self.q_reg[i] = self.q_reg[i - 1]
                # Input goes to Q[0]
                self.q_reg[0] = s_in

            # Multiplexer logic: ABC selects which Q bit becomes Z
            sel = (a << 2) | (b << 1) | c  # Combine ABC to form 3-bit selector
            self.z_out = self.q_reg[sel]

            # Convert output to binary string format
            z_bin = BinaryValue(value=self.z_out, n_bits=1)
            stimulus_outputs.append({"Z": z_bin.binstr})

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
