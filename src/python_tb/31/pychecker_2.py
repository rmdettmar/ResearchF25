import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize Q state register
        self.Q = BinaryValue("0")

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            L = BinaryValue(stimulus["L"])
            q_in = BinaryValue(stimulus["q_in"])
            r_in = BinaryValue(stimulus["r_in"])

            # Update Q based on L select signal
            if L.integer:
                self.Q = BinaryValue(r_in.binstr)
            else:
                self.Q = BinaryValue(q_in.binstr)

            # Append current output to results
            stimulus_outputs.append({"Q": self.Q.binstr})

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
