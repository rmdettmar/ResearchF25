import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state register
        """
        self.state_reg = 0  # Initialize state flip-flop to 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs based on sequential logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])
            clk_bv = BinaryValue(stimulus["clk"])

            # Convert to integer values
            a = a_bv.integer
            b = b_bv.integer
            clk = clk_bv.integer

            # Compute output q based on current state and inputs
            q = 1 if ((not a and b) or (not b and self.state_reg)) else 0

            # Update state on positive clock edge
            if clk == 1:
                self.state_reg = 1 if (a and b) else 0

            # Create output dictionary for this stimulus
            output = {"state": format(self.state_reg, "b"), "q": format(q, "b")}
            stimulus_outputs.append(output)

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
