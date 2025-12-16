import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the internal state Q register to 0
        """
        self.Q = BinaryValue("0")

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process input stimuli and update internal state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            L = BinaryValue(stimulus["L"])
            r_in = BinaryValue(stimulus["r_in"])
            q_in = BinaryValue(stimulus["q_in"])

            # Update state based on load signal
            if L.integer == 1:
                self.Q = BinaryValue(r_in.binstr)
            else:
                self.Q = BinaryValue(q_in.binstr)

            # Append current output to results
            stimulus_outputs.append({"Q": self.Q.binstr})

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
