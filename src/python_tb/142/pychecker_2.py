import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state register"""
        self.state_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            clk = BinaryValue(stimulus["clk"]).integer
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer

            # Update state on positive clock edge
            if clk == 1:
                if a == 1 and b == 1:
                    self.state_reg = 1 if self.state_reg == 0 else 0

            # Calculate output q based on current state and inputs
            if self.state_reg == 0:
                q = a ^ b  # XOR when state is 0
            else:
                q = not (a ^ b)  # XNOR when state is 1

            # Create output dictionary for this stimulus
            output = {"q": str(int(q)), "state": str(self.state_reg)}
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
