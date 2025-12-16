import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state Q to 0
        self.Q = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            j_val = BinaryValue(stimulus["j"])
            k_val = BinaryValue(stimulus["k"])

            # Get integer values
            j = j_val.integer
            k = k_val.integer

            # JK flip-flop logic
            if j == 0 and k == 0:
                # Hold state
                pass
            elif j == 0 and k == 1:
                # Clear
                self.Q = 0
            elif j == 1 and k == 0:
                # Set
                self.Q = 1
            else:  # j == 1 and k == 1
                # Toggle
                self.Q = 1 if self.Q == 0 else 0

            # Convert output to binary string
            q_out = BinaryValue(value=self.Q, n_bits=1)
            stimulus_outputs.append({"Q": q_out.binstr})

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
