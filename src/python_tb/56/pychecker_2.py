import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the internal state register q
        """
        self.q = 0
        self.prev_clk = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process input stimuli and update the flip-flop state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            clk_bv = BinaryValue(stimulus["clk"])
            d_bv = BinaryValue(stimulus["d"])

            # Convert to integer values
            clk = clk_bv.integer
            d = d_bv.integer

            # Check for clock edge (rising or falling)
            if (clk == 1 and self.prev_clk == 0) or (clk == 0 and self.prev_clk == 1):
                self.q = d

            # Update previous clock state
            self.prev_clk = clk

            # Convert output to binary string format
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
