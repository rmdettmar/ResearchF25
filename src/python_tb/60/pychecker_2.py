import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize counter to 0
        self.counter = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            reset = reset_bv.integer

            # Update counter based on reset and current value
            if reset:
                self.counter = 0
            else:
                if self.counter >= 999:
                    self.counter = 0
                else:
                    self.counter += 1

            # Convert counter value to 10-bit BinaryValue for output
            q_bv = BinaryValue(value=self.counter, n_bits=10)

            # Add output to results
            stimulus_outputs.append({"q": q_bv.binstr})

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
