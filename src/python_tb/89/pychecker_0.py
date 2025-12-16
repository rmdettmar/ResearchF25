import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize the 4-bit counter register to 0
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            reset = BinaryValue(stimulus["reset"]).integer

            # Update counter state
            if reset:
                self.q_reg = 0
            else:
                # Increment counter and wrap around at 16
                self.q_reg = (self.q_reg + 1) & 0xF

            # Convert output to 4-bit BinaryValue
            q_out = BinaryValue(value=self.q_reg, n_bits=4)

            # Append output to results
            stimulus_outputs.append({"q": q_out.binstr})

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
