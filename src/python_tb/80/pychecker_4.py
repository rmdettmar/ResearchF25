import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 5-bit LFSR state register
        """
        self.q_reg = BinaryValue(value=1, n_bits=5)

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update LFSR state based on input stimulus
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)

            if reset:
                # Synchronous reset - set to 1
                self.q_reg = BinaryValue(value=1, n_bits=5)
            else:
                # Get current state
                current_state = self.q_reg.integer

                # Get output bit (LSB)
                output_bit = current_state & 1

                # Calculate next state using Galois LFSR with taps at positions 5 and 3
                next_state = current_state >> 1

                # If output bit is 1, XOR with tap positions
                if output_bit:
                    next_state ^= 0b10100  # Taps at positions 5 (10000) and 3 (00100)

                # Update state register
                self.q_reg = BinaryValue(value=next_state, n_bits=5)

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
