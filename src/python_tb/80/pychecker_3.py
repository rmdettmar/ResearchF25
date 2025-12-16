import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 5-bit LFSR state register
        """
        self.q_reg = BinaryValue(value=1, n_bits=5)  # Initialize to 1 as per spec

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update LFSR state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to BinaryValue
            reset = int(stimulus["reset"], 2)

            if reset:
                # Synchronous reset to 1
                self.q_reg = BinaryValue(value=1, n_bits=5)
            else:
                # Get current state
                current_state = self.q_reg.integer

                # Calculate feedback bit (MSB)
                feedback = (current_state >> 4) & 1

                # Shift left by 1 and apply feedback with XOR at tap positions
                new_state = (current_state << 1) & 0x1F  # 5-bit mask
                # XOR tap at position 3
                if feedback:
                    new_state ^= 1 << 2  # XOR bit 3 (0-based index)
                # Set LSB to feedback
                new_state |= feedback

                # Update state register
                self.q_reg = BinaryValue(value=new_state, n_bits=5)

            # Format output as binary string
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
