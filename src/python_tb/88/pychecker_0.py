import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize counter to track cycles after reset
        self.counter = 0
        self.shift_ena = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer

            # Handle reset
            if reset:
                self.counter = 4
            elif self.counter > 0:
                self.counter -= 1

            # Generate shift_ena output
            self.shift_ena = 1 if self.counter > 0 else 0

            # Convert output to binary string format
            shift_ena_bv = BinaryValue(value=self.shift_ena, n_bits=1)

            # Add outputs to list
            stimulus_outputs.append({"shift_ena": shift_ena_bv.binstr})

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
