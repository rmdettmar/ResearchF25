import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 32-bit LFSR state register
        self.q_reg = 1  # Initial state after reset

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer

            if reset:
                # Synchronous reset - set to 32'h1
                self.q_reg = 1
            else:
                # Galois LFSR operation
                current_state = self.q_reg
                output_bit = (current_state >> 31) & 1  # MSB

                # Calculate next state
                next_state = current_state << 1  # Shift left by 1

                # Apply taps (XOR with output bit at positions 32,22,2,1)
                if output_bit:
                    next_state ^= 1 << 31  # Position 32
                    next_state ^= 1 << 21  # Position 22
                    next_state ^= 1 << 1  # Position 2
                    next_state ^= 1  # Position 1

                # Ensure 32-bit value
                self.q_reg = next_state & 0xFFFFFFFF

            # Convert output to 32-bit binary string
            output_value = BinaryValue(value=self.q_reg, n_bits=32)
            stimulus_outputs.append({"q": output_value.binstr})

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
