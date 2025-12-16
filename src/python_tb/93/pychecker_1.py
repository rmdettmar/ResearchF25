import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 4-bit counter to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings to values
            reset = BinaryValue(stimulus["reset"]).integer

            if reset:
                # Synchronous reset - set counter to 0
                self.q_reg = 0
            else:
                # Increment counter if not at 9, wrap to 0 if at 9
                self.q_reg = 0 if self.q_reg == 9 else self.q_reg + 1

            # Convert the 4-bit counter value to binary string format
            q_bv = BinaryValue(value=self.q_reg, n_bits=4)

            # Add the output to the list
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
