import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 100-bit register to 0
        self.q_reg = BinaryValue(value=0, n_bits=100)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            load_bv = BinaryValue(stimulus["load"])
            ena_bv = BinaryValue(stimulus["ena"])
            data_bv = BinaryValue(stimulus["data"])

            # Get integer values
            load = load_bv.integer
            ena = ena_bv.integer
            data = data_bv.integer
            current_q = self.q_reg.integer

            if load:
                # Synchronous load
                self.q_reg = BinaryValue(value=data, n_bits=100)
            else:
                if ena == 0b01:  # Right rotation
                    # Save LSB and shift right
                    lsb = current_q & 1
                    rotated = (current_q >> 1) | (lsb << 99)
                    self.q_reg = BinaryValue(value=rotated, n_bits=100)
                elif ena == 0b10:  # Left rotation
                    # Save MSB and shift left
                    msb = (current_q >> 99) & 1
                    rotated = ((current_q << 1) & ((1 << 100) - 1)) | msb
                    self.q_reg = BinaryValue(value=rotated, n_bits=100)
                # For ena=00 or ena=11, no rotation occurs

            # Add current output to list
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
