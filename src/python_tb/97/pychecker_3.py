import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state register to 000
        """
        self.state = 0  # 3-bit state register
        self.z = 0  # output register

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Update state and output based on inputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            reset = int(BinaryValue(stimulus["reset"]).value)
            x = int(BinaryValue(stimulus["x"]).value)

            # Update state based on reset or state transition table
            if reset:
                self.state = 0  # Reset to 000
            else:
                # Implement state transition table
                if self.state == 0b000:
                    self.state = 0b001 if x else 0b000
                elif self.state == 0b001:
                    self.state = 0b100 if x else 0b001
                elif self.state == 0b010:
                    self.state = 0b001 if x else 0b010
                elif self.state == 0b011:
                    self.state = 0b010 if x else 0b001
                elif self.state == 0b100:
                    self.state = 0b100 if x else 0b011

            # Update output z based on current state
            self.z = 1 if self.state in [0b011, 0b100] else 0

            # Append output to results
            stimulus_outputs.append({"z": str(self.z)})

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
