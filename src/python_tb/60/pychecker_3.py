import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize counter to 0
        """
        self.counter = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Update counter based on reset input
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert reset string to BinaryValue
            reset_bv = BinaryValue(stimulus["reset"])
            reset = reset_bv.integer

            # Update counter
            if reset:
                self.counter = 0
            else:
                self.counter = (self.counter + 1) if self.counter < 999 else 0

            # Convert counter to 10-bit BinaryValue for output
            q_bv = BinaryValue(value=self.counter, n_bits=10)
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
