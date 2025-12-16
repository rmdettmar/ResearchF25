import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables:
        - ones_count: number of consecutive 1s seen
        - disc_reg: registered discard signal
        - flag_reg: registered flag signal
        - err_reg: registered error signal
        """
        self.ones_count = 0
        self.disc_reg = 0
        self.flag_reg = 0
        self.err_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to BinaryValue
            reset = BinaryValue(stimulus["reset"]).integer
            in_bit = BinaryValue(stimulus["in"]).integer

            # Handle reset
            if reset:
                self.ones_count = 0
                self.disc_reg = 0
                self.flag_reg = 0
                self.err_reg = 0
            else:
                # Update outputs based on previous state
                if self.ones_count == 5 and in_bit == 0:
                    self.disc_reg = 1
                    self.flag_reg = 0
                    self.err_reg = 0
                elif self.ones_count == 6 and in_bit == 0:
                    self.disc_reg = 0
                    self.flag_reg = 1
                    self.err_reg = 0
                elif self.ones_count >= 7:
                    self.disc_reg = 0
                    self.flag_reg = 0
                    self.err_reg = 1
                else:
                    self.disc_reg = 0
                    self.flag_reg = 0
                    self.err_reg = 0

                # Update ones counter
                if in_bit == 1:
                    self.ones_count += 1
                else:
                    self.ones_count = 0

            # Prepare output dictionary
            output = {
                "disc": format(self.disc_reg, "b"),
                "flag": format(self.flag_reg, "b"),
                "err": format(self.err_reg, "b"),
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
