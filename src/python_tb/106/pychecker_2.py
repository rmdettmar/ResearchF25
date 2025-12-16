import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize state registers"""
        self.p_reg = 0  # Output p state register
        self.q_reg = 0  # Output q state register
        self.prev_clk = 0  # Previous clock value for edge detection

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            clk = BinaryValue(stimulus["clock"]).integer
            a = BinaryValue(stimulus["a"]).integer

            # Detect rising clock edge
            if clk == 1 and self.prev_clk == 0:
                # Update p to match input a
                self.p_reg = a
                # Update q to match previous p
                self.q_reg = self.p_reg

            # Store current clock for next iteration
            self.prev_clk = clk

            # Create output dictionary for this stimulus
            output = {
                "p": BinaryValue(value=self.p_reg, n_bits=1).binstr,
                "q": BinaryValue(value=self.q_reg, n_bits=1).binstr,
            }
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
