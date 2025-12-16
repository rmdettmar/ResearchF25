import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize 256-bit state register
        self.q_reg = 0

    def get_cell(self, state, x, y):
        # Get cell value at x,y coordinates with wraparound
        x = x % 16
        y = y % 16
        idx = y * 16 + x
        return (state >> idx) & 1

    def count_neighbors(self, state, x, y):
        # Count live neighbors including wraparound
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                count += self.get_cell(state, x + dx, y + dy)
        return count

    def next_state(self, state, x, y):
        # Determine next state based on neighbor count
        neighbors = self.count_neighbors(state, x, y)
        current = self.get_cell(state, x, y)

        if neighbors <= 1:
            return 0
        elif neighbors == 2:
            return current
        elif neighbors == 3:
            return 1
        else:  # neighbors >= 4
            return 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load = int(stimulus["load"], 2)
            data = int(stimulus["data"], 2)

            if load:
                self.q_reg = data
            else:
                # Calculate next state for each cell
                next_state = 0
                for y in range(16):
                    for x in range(16):
                        if self.next_state(self.q_reg, x, y):
                            idx = y * 16 + x
                            next_state |= 1 << idx
                self.q_reg = next_state

            # Format output as binary string
            stimulus_outputs.append(format(self.q_reg, "0256b"))

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
