import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the counter state to 1
        """
        self.q_reg = 1  # Counter starts at 1

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input stimuli and update counter state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary string inputs to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            reset = reset_bv.integer

            if reset:
                self.q_reg = 1  # Synchronous reset to 1
            else:
                # Increment counter if less than 10
                if self.q_reg < 10:
                    self.q_reg += 1
                else:
                    self.q_reg = 1  # Wrap around to 1 after 10

            # Convert output to 4-bit BinaryValue
            q_bv = BinaryValue(value=self.q_reg, n_bits=4)

            # Add current output to results
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
