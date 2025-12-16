import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 5-bit LFSR state register
        """
        self.q_reg = BinaryValue(value=1, n_bits=5)  # Initialize to 1

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Update LFSR state based on input stimulus
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)  # Convert binary string to int

            if reset:
                self.q_reg = BinaryValue(value=1, n_bits=5)
            else:
                # Get current state
                current_state = self.q_reg.integer

                # Calculate next state
                # Rightmost bit (bit 0) is used for feedback
                feedback = current_state & 1

                # Shift right and apply feedback to tap positions (5 and 3)
                next_state = current_state >> 1
                if feedback:
                    # XOR with taps at positions 5 (bit 4) and 3 (bit 2)
                    next_state ^= 1 << 4  # Tap at bit 4 (position 5)
                    next_state ^= 1 << 2  # Tap at bit 2 (position 3)

                # Update state register
                self.q_reg = BinaryValue(value=next_state, n_bits=5)

            # Convert current state to binary string for output
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
