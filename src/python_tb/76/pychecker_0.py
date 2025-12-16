import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 8-bit register to 0
        """
        self.q_reg = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process input stimuli and update internal state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Update state based on reset condition
            if reset:
                self.q_reg = BinaryValue(value=0, n_bits=8)
            else:
                self.q_reg = BinaryValue(value=d, n_bits=8)

            # Add current output to results
            stimulus_outputs.append({"q": self.q_reg.binstr})

        # Return formatted output dictionary
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
