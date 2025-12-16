import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize 256-bit state register
        self.q_reg = 0

    def _get_cell(self, state, row, col):
        # Handle toroidal wrapping
        row = row % 16
        col = col % 16
        idx = row * 16 + col
        return (state >> idx) & 1

    def _count_neighbors(self, state, row, col):
        count = 0
        # Check all 8 neighboring cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                count += self._get_cell(state, row + dr, col + dc)
        return count

    def _calculate_next_state(self):
        next_state = 0
        current_state = self.q_reg

        for row in range(16):
            for col in range(16):
                neighbors = self._count_neighbors(current_state, row, col)
                current_cell = self._get_cell(current_state, row, col)

                # Apply Game of Life rules
                new_cell = 0
                if neighbors == 2:
                    new_cell = current_cell
                elif neighbors == 3:
                    new_cell = 1

                # Set the bit in the next state
                if new_cell:
                    next_state |= 1 << (row * 16 + col)

        return next_state

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load_signal = int(stimulus["load"], 2)
            data = int(stimulus["data"], 2)

            if load_signal:
                self.q_reg = data
            else:
                self.q_reg = self._calculate_next_state()

            # Format output as binary string
            q_str = format(self.q_reg, "0256b")
            stimulus_outputs.append({"q": q_str})

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
