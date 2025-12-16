import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register to 1 (32'h1)
        self.q_reg = 1

    def _calculate_next_state(self, current_state):
        # Get the output bit (LSB)
        output_bit = current_state & 1

        # Calculate feedback based on taps at positions 32, 22, 2, and 1
        # Note: positions are 1-based, so subtract 1 for 0-based indexing
        feedback = output_bit
        feedback ^= (current_state >> 31) & 1  # Position 32
        feedback ^= (current_state >> 21) & 1  # Position 22
        feedback ^= (current_state >> 1) & 1  # Position 2

        # Shift right and place feedback in MSB
        next_state = (current_state >> 1) | (feedback << 31)
        return next_state & 0xFFFFFFFF  # Ensure 32-bit value

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue for proper handling
            reset_signal = BinaryValue(stimulus["reset"])

            # Update state based on reset and clock
            if reset_signal.integer:
                self.q_reg = 1  # Reset to 32'h1
            else:
                self.q_reg = self._calculate_next_state(self.q_reg)

            # Convert output to binary string format
            q_bv = BinaryValue(value=self.q_reg, n_bits=32)
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
