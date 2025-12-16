import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize Q output to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            j = BinaryValue(stimulus["j"]).integer
            k = BinaryValue(stimulus["k"]).integer
            q_old = self.q_reg

            # Implement JK flip-flop truth table
            if j == 0 and k == 0:
                self.q_reg = q_old  # No change
            elif j == 0 and k == 1:
                self.q_reg = 0  # Reset
            elif j == 1 and k == 0:
                self.q_reg = 1  # Set
            else:  # j == 1 and k == 1
                self.q_reg = 1 if q_old == 0 else 0  # Toggle

            # Convert output to binary string format
            q_out = BinaryValue(value=self.q_reg, n_bits=1)
            stimulus_outputs.append({"Q": q_out.binstr})

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
