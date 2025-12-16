import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 256-bit state register
        self.q_reg = BinaryValue(value=0, n_bits=256)

    def get_neighbor_count(self, row: int, col: int) -> int:
        count = 0
        # Check all 8 neighbors with wrap-around
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                # Handle wrap-around
                neighbor_row = (row + i) % 16
                neighbor_col = (col + j) % 16
                # Calculate bit position
                bit_pos = neighbor_row * 16 + neighbor_col
                if self.q_reg[bit_pos] == 1:
                    count += 1
        return count

    def update_cell(self, neighbors: int, current_state: int) -> int:
        if neighbors <= 1 or neighbors >= 4:
            return 0
        elif neighbors == 2:
            return current_state
        else:  # neighbors == 3
            return 1

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load_signal = int(stimulus["load"], 2)
            data = BinaryValue(value=int(stimulus["data"], 2), n_bits=256)

            if load_signal:
                # Load new state
                self.q_reg = data
            else:
                # Calculate next state for each cell
                next_state = BinaryValue(value=0, n_bits=256)
                for row in range(16):
                    for col in range(16):
                        bit_pos = row * 16 + col
                        neighbor_count = self.get_neighbor_count(row, col)
                        current_cell = self.q_reg[bit_pos]
                        next_cell = self.update_cell(neighbor_count, current_cell)
                        next_state[bit_pos] = next_cell
                self.q_reg = next_state

            # Add current state to outputs
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
