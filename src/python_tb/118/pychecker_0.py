import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize FSM state and counters
        """
        self.state = 0  # A=0, B=1
        self.cycle_count = 0  # Count 3 cycles
        self.w_count = 0  # Count w=1 occurrences
        self.z = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Update FSM state and generate output based on inputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to integers
            reset = BinaryValue(stimulus["reset"]).integer
            s = BinaryValue(stimulus["s"]).integer
            w = BinaryValue(stimulus["w"]).integer

            if reset:
                self.state = 0
                self.cycle_count = 0
                self.w_count = 0
                self.z = 0
            else:
                if self.state == 0:  # State A
                    if s == 1:
                        self.state = 1  # Move to state B
                        self.cycle_count = 0
                        self.w_count = 0
                else:  # State B
                    if w == 1:
                        self.w_count += 1
                    self.cycle_count += 1

                    if self.cycle_count == 3:
                        self.z = 1 if self.w_count == 2 else 0
                        self.cycle_count = 0
                        self.w_count = 0

            # Convert output to binary string
            z_bv = BinaryValue(value=self.z, n_bits=1)
            stimulus_outputs.append({"z": z_bv.binstr})

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
