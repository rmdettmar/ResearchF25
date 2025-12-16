import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 100-bit register to 0
        """
        self.q_reg = BinaryValue(value=0, n_bits=100)

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimuli and update internal state
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            load = int(stimulus["load"], 2)
            ena = int(stimulus["ena"], 2)
            data = BinaryValue(value=stimulus["data"], n_bits=100)

            if load:
                # Synchronous load
                self.q_reg = data
            else:
                # Rotation logic
                current_q = self.q_reg.binstr
                if ena == 0b01:  # Rotate right
                    self.q_reg = BinaryValue(
                        value=current_q[-1] + current_q[:-1], n_bits=100
                    )
                elif ena == 0b10:  # Rotate left
                    self.q_reg = BinaryValue(
                        value=current_q[1:] + current_q[0], n_bits=100
                    )
                # For ena=00 or ena=11, no rotation occurs

            # Add current output to results
            stimulus_outputs.append({"q": self.q_reg.binstr})

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
