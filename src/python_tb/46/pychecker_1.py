import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register
        self.q_reg = 1  # Reset value is 32'h1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            reset = int(BinaryValue(stimulus["reset"]).value)

            if reset:
                # Synchronous reset - set to 32'h1
                self.q_reg = 1
            else:
                # Compute next state
                # Get the LSB (output bit)
                output_bit = self.q_reg & 1

                # Create the next state by shifting right
                next_state = self.q_reg >> 1

                # Apply XOR at tap positions (32, 22, 2, 1)
                # For position 32 (MSB), XOR with output_bit
                if output_bit:
                    next_state ^= 1 << 31  # Position 32 (0-based index)

                # For position 22
                if output_bit:
                    next_state ^= 1 << 21  # Position 22 (0-based index)

                # For position 2
                if output_bit:
                    next_state ^= 1 << 1  # Position 2 (0-based index)

                # For position 1
                if output_bit:
                    next_state ^= 1 << 0  # Position 1 (0-based index)

                # Update state register
                self.q_reg = next_state & 0xFFFFFFFF  # Ensure 32-bit value

            # Convert output to binary string format
            q_bv = BinaryValue(value=self.q_reg, n_bits=32, bigEndian=True)
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
