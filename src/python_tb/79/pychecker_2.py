import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            clk = int(stimulus["clk"])
            a = int(stimulus["a"])

            # Only update on rising clock edge (clk = 1)
            if clk == 1:
                if a == 1:
                    # When a is 1, q is fixed at 4
                    self.q_reg = 4
                else:
                    # When a is 0, increment q, wrapping around after 6
                    self.q_reg = (self.q_reg + 1) % 7

            # Create output dictionary for this stimulus
            # Convert q_reg to 3-bit BinaryValue
            q_bv = BinaryValue(value=self.q_reg, n_bits=3)
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
