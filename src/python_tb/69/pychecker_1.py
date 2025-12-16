import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state variables
        """
        self.Y0 = 0  # LSB of next state
        self.z = 0  # Output signal

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and calculate outputs according to state table
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Calculate Y0 (LSB of next state) based on current state and input
            if y == 0b000:
                self.Y0 = 1 if x else 0
            elif y == 0b001:
                self.Y0 = 0 if x else 1
            elif y == 0b010:
                self.Y0 = 1 if x else 0
            elif y == 0b011:
                self.Y0 = 0 if x else 1
            elif y == 0b100:
                self.Y0 = 0 if x else 1

            # Calculate output z based on current state
            self.z = 1 if (y == 0b011 or y == 0b100) else 0

            # Append outputs to results
            stimulus_outputs.append(
                {"Y0": format(self.Y0, "b"), "z": format(self.z, "b")}
            )

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
