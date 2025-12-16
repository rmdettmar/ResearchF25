import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 5-bit LFSR state register
        self.q_reg = BinaryValue(value=1, n_bits=5)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            reset = int(stimulus["reset"], 2)

            if reset:
                # Reset condition - set LFSR to 1
                self.q_reg = BinaryValue(value=1, n_bits=5)
            else:
                # LFSR operation
                current_state = self.q_reg.integer
                # Get the output bit (MSB)
                output_bit = (current_state >> 4) & 1
                # Calculate next state
                # Shift left by 1 and XOR with tapped positions
                next_state = (current_state << 1) & 0x1F
                if output_bit:
                    # XOR with tap positions (5 and 3)
                    next_state ^= 0x5  # Binary 00101 for positions 5 and 3

                self.q_reg = BinaryValue(value=next_state, n_bits=5)

            # Add current state to outputs
            stimulus_outputs.append({"q": self.q_reg.binstr})

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
