import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.q_reg = 0
        self.prev_clk = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            clk_bv = BinaryValue(stimulus["clk"])
            d_bv = BinaryValue(stimulus["d"])

            # Get integer values
            clk = clk_bv.integer
            d = d_bv.integer

            # Check for clock edge (both rising and falling)
            if clk != self.prev_clk:
                # Update q on any clock edge
                self.q_reg = d

            # Store current clock for next cycle
            self.prev_clk = clk

            # Create output dictionary for this stimulus
            output = {"q": format(self.q_reg, "b")}
            stimulus_outputs.append(output)

        # Return formatted output dictionary
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
