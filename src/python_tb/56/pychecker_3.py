import json
from typing import Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.pos_reg = 0  # Register for positive edge
        self.neg_reg = 0  # Register for negative edge
        self.q = 0  # Output register
        self.prev_clk = 0  # Track previous clock value

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            clk = BinaryValue(stimulus["clk"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Detect clock edge
            if clk != self.prev_clk:
                if clk == 1:  # Rising edge
                    self.pos_reg = d
                    self.q = d
                else:  # Falling edge
                    self.neg_reg = d
                    self.q = d

            # Update previous clock value
            self.prev_clk = clk

            # Format output as binary string
            q_bv = BinaryValue(value=self.q, n_bits=1)
            stimulus_outputs.append({"q": q_bv.binstr})

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
