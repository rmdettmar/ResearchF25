import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the flip-flop output to 0
        self.Q = BinaryValue("0")

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        # Process each stimulus in the input
        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            L = BinaryValue(stimulus["L"]).integer
            q_in = BinaryValue(stimulus["q_in"]).integer
            r_in = BinaryValue(stimulus["r_in"]).integer

            # Update state based on L (load) signal
            if L:
                self.Q = BinaryValue(value=r_in, n_bits=1)
            else:
                self.Q = BinaryValue(value=q_in, n_bits=1)

            # Add the output to the list
            stimulus_outputs.append({"Q": self.Q.binstr})

        # Format the output dictionary
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
