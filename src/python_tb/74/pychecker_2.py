import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize internal counter state
        self.counter = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signals
            load = int(stimulus["load"])
            data_bv = BinaryValue(stimulus["data"], n_bits=10)
            data = data_bv.integer

            # Update counter based on load signal
            if load:
                self.counter = data
            elif self.counter > 0:
                self.counter = self.counter - 1

            # Generate tc output
            tc = 1 if self.counter == 0 else 0

            # Add output to list
            stimulus_outputs.append({"tc": str(tc)})

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
