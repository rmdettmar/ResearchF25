import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state register q
        """
        self.q = 0
        self.prev_clk = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to counter logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to appropriate format
            clk = int(stimulus["clk"], 2)
            a = int(stimulus["a"], 2)

            # Only update on positive clock edge
            if clk == 1 and self.prev_clk == 0:
                if a == 1:
                    self.q = 4  # Hold at 4 when a is 1
                else:
                    # When a is 0, increment counter
                    self.q = (self.q + 1) if self.q < 6 else 0

            # Update previous clock state
            self.prev_clk = clk

            # Convert output to 3-bit binary string
            q_bv = BinaryValue(value=self.q, n_bits=3, bigEndian=False)

            # Add output to results
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
