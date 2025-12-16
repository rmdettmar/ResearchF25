import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 256-bit state register
        self.q_reg = 0

    def _get_cell(self, grid, x, y):
        # Handle wraparound for toroidal grid
        x = x % 16
        y = y % 16
        return (grid >> (y * 16 + x)) & 1

    def _count_neighbors(self, grid, x, y):
        count = 0
        # Check all 8 neighbors with wraparound
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                count += self._get_cell(grid, x + dx, y + dy)
        return count

    def _calculate_next_state(self, current_state):
        next_state = 0
        # Process each cell in the 16x16 grid
        for y in range(16):
            for x in range(16):
                current_cell = self._get_cell(current_state, x, y)
                neighbors = self._count_neighbors(current_state, x, y)

                # Apply Game of Life rules
                new_cell = 0
                if neighbors == 2:
                    new_cell = current_cell
                elif neighbors == 3:
                    new_cell = 1
                # else: cell becomes 0 (already initialized to 0)

                # Set the bit in the next state
                if new_cell:
                    next_state |= 1 << (y * 16 + x)
        return next_state

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []
        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to integers
            load_bv = BinaryValue(stimulus["load"])
            data_bv = BinaryValue(stimulus["data"])

            if load_bv.integer:
                # Load new data
                self.q_reg = data_bv.integer & ((1 << 256) - 1)
            else:
                # Calculate next generation
                self.q_reg = self._calculate_next_state(self.q_reg)

            # Convert output to binary string
            out_bv = BinaryValue(value=self.q_reg, n_bits=256)
            stimulus_outputs.append(out_bv.binstr)

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
