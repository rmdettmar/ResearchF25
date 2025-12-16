import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 32-bit LFSR state register to 1
        self.q_reg = 1

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer

            if reset:
                # Synchronous reset - set q to 1
                self.q_reg = 1
            else:
                # LFSR operation
                # Get current state
                current_state = self.q_reg

                # Calculate feedback based on tap positions (32,22,2,1)
                # Note: positions are counted from 1, so subtract 1 for 0-based indexing
                tap32 = (current_state >> 31) & 1  # MSB
                tap22 = (current_state >> 21) & 1
                tap2 = (current_state >> 1) & 1
                tap1 = current_state & 1  # LSB

                # Calculate feedback (XOR of all taps)
                feedback = tap32 ^ tap22 ^ tap2 ^ tap1

                # Shift right and set MSB to feedback
                self.q_reg = ((current_state >> 1) | (feedback << 31)) & 0xFFFFFFFF

            # Convert output to 32-bit binary string
            q_binary = format(self.q_reg, "032b")
            stimulus_outputs.append({"q": q_binary})

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
