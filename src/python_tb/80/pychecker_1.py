import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 5-bit LFSR state register
        self.q_reg = 1  # Initial state (non-zero)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings
            reset = int(BinaryValue(stimulus["reset"]).value)

            if reset:
                # Synchronous reset - set to 1
                self.q_reg = 1
            else:
                # LFSR operation
                current_state = self.q_reg
                # Get the feedback bit (XOR of output bit and tap position 3)
                feedback = ((current_state >> 4) ^ (current_state >> 2)) & 1
                # Shift the register
                next_state = (current_state << 1) & 0x1F  # Keep 5 bits
                # Apply feedback to bit 0
                next_state |= feedback
                self.q_reg = next_state

            # Convert output to 5-bit binary string
            out_q = BinaryValue(value=self.q_reg, n_bits=5)
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
