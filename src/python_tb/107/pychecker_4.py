import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 512-bit q register to 0
        self.q_reg = BinaryValue(value=0, n_bits=512)

    def _calc_next_state(self, left: int, right: int) -> int:
        # Rule 90: next state is XOR of left and right neighbors
        return left ^ right

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            load = int(stimulus["load"], 2)
            data = BinaryValue(value=int(stimulus["data"], 2), n_bits=512)

            if load:
                # Synchronous load
                self.q_reg = data
            else:
                # Calculate next state for each cell
                next_state = BinaryValue(value=0, n_bits=512)
                current_state = self.q_reg

                # Handle all cells
                for i in range(512):
                    # Get left neighbor (0 for leftmost cell)
                    left = 0 if i == 0 else int(current_state[i - 1])
                    # Get right neighbor (0 for rightmost cell)
                    right = 0 if i == 511 else int(current_state[i + 1])
                    # Calculate next state for this cell
                    next_bit = self._calc_next_state(left, right)
                    # Set the bit in next state
                    if next_bit:
                        next_state[i] = 1

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
