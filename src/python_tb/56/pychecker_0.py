import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register
        self.q = BinaryValue("0", n_bits=1)
        self.prev_clk = BinaryValue("0", n_bits=1)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            clk = BinaryValue(stimulus["clk"], n_bits=1)
            d = BinaryValue(stimulus["d"], n_bits=1)

            # Check for clock edge (both rising and falling)
            if clk.integer != self.prev_clk.integer:
                # Update q on any clock edge
                self.q = BinaryValue(d.binstr, n_bits=1)

            # Update previous clock value
            self.prev_clk = clk

            # Add current output to stimulus_outputs
            stimulus_outputs.append({"q": self.q.binstr})

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
