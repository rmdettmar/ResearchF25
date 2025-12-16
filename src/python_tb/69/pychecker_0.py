import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = 0  # Initialize to state 000

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input values
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Calculate next state based on current y and x
            next_state = self.calculate_next_state(y, x)

            # Calculate output z based on current state
            z = 1 if y in [0b011, 0b100] else 0

            # Y0 is the least significant bit of next state
            Y0 = next_state & 1

            # Create output dictionary
            output = {"Y0": format(Y0, "b"), "z": format(z, "b")}
            stimulus_outputs.append(output)

        return {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

    def calculate_next_state(self, current_state: int, x: int) -> int:
        """Helper method to calculate next state"""
        if x == 0:
            if current_state == 0b000:
                return 0b000
            elif current_state == 0b001:
                return 0b001
            elif current_state == 0b010:
                return 0b010
            elif current_state == 0b011:
                return 0b001
            elif current_state == 0b100:
                return 0b011
        else:  # x == 1
            if current_state == 0b000:
                return 0b001
            elif current_state == 0b001:
                return 0b100
            elif current_state == 0b010:
                return 0b001
            elif current_state == 0b011:
                return 0b010
            elif current_state == 0b100:
                return 0b100
        return 0b000  # Default case


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
