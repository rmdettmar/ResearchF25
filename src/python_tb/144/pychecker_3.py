import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize FSM state and output registers
        """
        self.ones_count = 0  # Track consecutive 1s
        self.prev_in = 0  # Previous input value
        self.disc_reg = 0  # Zero insertion needed
        self.flag_reg = 0  # Frame boundary detected
        self.err_reg = 0  # Error condition detected

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process inputs and generate outputs according to HDLC framing rules
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to integers
            reset = int(BinaryValue(stimulus["reset"]).integer)
            in_bit = int(BinaryValue(stimulus["in"]).integer)

            # Update state and outputs
            if reset:
                self.ones_count = 0
                self.prev_in = 0
                self.disc_reg = 0
                self.flag_reg = 0
                self.err_reg = 0
            else:
                # Update outputs based on previous state
                if in_bit == 1:
                    if self.ones_count < 7:
                        self.ones_count += 1
                    if self.ones_count >= 7:
                        self.err_reg = 1
                        self.disc_reg = 0
                        self.flag_reg = 0
                else:  # in_bit == 0
                    if self.ones_count == 5:
                        self.disc_reg = 1
                        self.flag_reg = 0
                        self.err_reg = 0
                    elif self.ones_count == 6:
                        self.flag_reg = 1
                        self.disc_reg = 0
                        self.err_reg = 0
                    else:
                        self.disc_reg = 0
                        self.flag_reg = 0
                        self.err_reg = 0
                    self.ones_count = 0

            # Store current outputs
            output_dict = {
                "disc": str(self.disc_reg),
                "flag": str(self.flag_reg),
                "err": str(self.err_reg),
            }
            outputs.append(output_dict)

            # Update previous input
            self.prev_in = in_bit

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
