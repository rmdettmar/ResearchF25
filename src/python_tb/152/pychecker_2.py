import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 16x16 grid state
        self.grid_state = BinaryValue(value=0, n_bits=256)

    def _get_cell(self, row: int, col: int) -> int:
        # Get cell value with toroidal wrapping
        row = row % 16
        col = col % 16
        idx = row * 16 + col
        return int(self.grid_state[idx])

    def _count_neighbors(self, row: int, col: int) -> int:
        # Count live neighbors with toroidal wrapping
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                neighbor_row = (row + dr) % 16
                neighbor_col = (col + dc) % 16
                count += self._get_cell(neighbor_row, neighbor_col)
        return count

    def _calculate_next_state(self):
        # Calculate next state for entire grid
        next_state = 0
        for row in range(16):
            for col in range(16):
                idx = row * 16 + col
                neighbors = self._count_neighbors(row, col)
                current_cell = self._get_cell(row, col)

                # Apply Game of Life rules
                new_cell = 0
                if neighbors == 2:
                    new_cell = current_cell
                elif neighbors == 3:
                    new_cell = 1

                if new_cell:
                    next_state |= 1 << idx

        return next_state

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load_signal = int(stimulus["load"], 2)
            data = int(stimulus["data"], 2)

            if load_signal:
                # Load new data into grid
                self.grid_state = BinaryValue(value=data, n_bits=256)
            else:
                # Calculate next generation
                next_state = self._calculate_next_state()
                self.grid_state = BinaryValue(value=next_state, n_bits=256)

            # Append current state to outputs
            stimulus_outputs.append({"q": self.grid_state.binstr})

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
