import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register to 0x34 (default reset value)
        self.q_reg = 0x34

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            d_bv = BinaryValue(stimulus["d"])
            clk_bv = BinaryValue(stimulus["clk"])

            # Check for negative edge of clock (transition from 1 to 0)
            if clk_bv.binstr == "0":
                if reset_bv.integer == 1:
                    # Synchronous reset to 0x34
                    self.q_reg = 0x34
                else:
                    # On negative edge, capture input d
                    self.q_reg = d_bv.integer

            # Create output dictionary for this stimulus
            q_bv = BinaryValue(value=self.q_reg, n_bits=8)
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
