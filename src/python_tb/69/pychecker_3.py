import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        self.current_state = 0  # 3-bit state register

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            x = BinaryValue(stimulus["x"]).integer
            y = BinaryValue(stimulus["y"]).integer

            # Calculate next state based on current state and input x
            next_state = self.calculate_next_state(y, x)

            # Calculate outputs
            Y0 = next_state & 1  # LSB of next state
            z = 1 if (y == 0b011 or y == 0b100) else 0

            # Convert outputs to binary strings
            Y0_bin = BinaryValue(value=Y0, n_bits=1).binstr
            z_bin = BinaryValue(value=z, n_bits=1).binstr

            # Add outputs to result list
            stimulus_outputs.append({"Y0": Y0_bin, "z": z_bin})

        return {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

    def calculate_next_state(self, current_state: int, x: int) -> int:
        """Helper method to determine next state"""
        if x == 0:
            # Next state for x=0
            next_state_table = {
                0b000: 0b000,
                0b001: 0b001,
                0b010: 0b010,
                0b011: 0b001,
                0b100: 0b011,
            }
        else:
            # Next state for x=1
            next_state_table = {
                0b000: 0b001,
                0b001: 0b100,
                0b010: 0b001,
                0b011: 0b010,
                0b100: 0b100,
            }

        return next_state_table.get(current_state, 0)


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
