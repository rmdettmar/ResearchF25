import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize the 512-bit state register
        """
        self.q_reg = BinaryValue(value=0, n_bits=512)

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and update state according to Rule 90
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            load = int(stimulus["load"], 2)
            data = BinaryValue(stimulus["data"])

            if load:
                # Load new data into register
                self.q_reg = data
            else:
                # Apply Rule 90: next state is XOR of left and right neighbors
                current_state = self.q_reg.binstr
                next_state = ["0"] * 512

                # Process each cell
                for i in range(512):
                    # Get left neighbor (0 if i=0)
                    left = "0" if i == 0 else current_state[i - 1]
                    # Get right neighbor (0 if i=511)
                    right = "0" if i == 511 else current_state[i + 1]
                    # XOR of neighbors
                    next_state[i] = "1" if left != right else "0"

                # Update state register
                self.q_reg = BinaryValue("".join(next_state))

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
