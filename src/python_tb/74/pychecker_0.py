import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the internal counter state to 0
        """
        self.counter = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update counter state according to timer specification
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue objects
            load_bv = BinaryValue(stimulus["load"])
            data_bv = BinaryValue(stimulus["data"])

            # Extract integer values
            load = load_bv.integer
            data = data_bv.integer

            # Update counter based on load signal
            if load:
                self.counter = data
            elif self.counter > 0:
                self.counter -= 1

            # Generate tc output
            tc = 1 if self.counter == 0 else 0

            # Convert output to binary string and append to results
            tc_bv = BinaryValue(value=tc, n_bits=1)
            stimulus_outputs.append({"tc": tc_bv.binstr})

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
