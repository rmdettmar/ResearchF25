import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.ones_count = 0  # Track consecutive 1s
        self.disc_reg = 0  # Zero insertion detected
        self.flag_reg = 0  # Frame boundary detected
        self.err_reg = 0  # Error condition detected

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to proper format
            reset = int(stimulus["reset"], 2)
            in_bit = int(stimulus["in"], 2)

            # Handle synchronous reset
            if reset:
                self.ones_count = 0
                self.disc_reg = 0
                self.flag_reg = 0
                self.err_reg = 0
            else:
                # Update state based on input
                if in_bit == 1:
                    self.ones_count += 1
                else:
                    # Check conditions when 0 is received
                    if self.ones_count == 5:
                        self.disc_reg = 1  # Signal bit discard
                    elif self.ones_count == 6:
                        self.flag_reg = 1  # Signal frame boundary
                    self.ones_count = 0

                # Check for error condition (7 or more 1s)
                if self.ones_count >= 7:
                    self.err_reg = 1
                    self.ones_count = 0

                # Reset other outputs if not currently active
                if self.ones_count != 5:
                    self.disc_reg = 0
                if self.ones_count != 6:
                    self.flag_reg = 0
                if self.ones_count < 7:
                    self.err_reg = 0

            # Format outputs
            outputs = {
                "disc": format(self.disc_reg, "b"),
                "flag": format(self.flag_reg, "b"),
                "err": format(self.err_reg, "b"),
            }
            stimulus_outputs.append(outputs)

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
