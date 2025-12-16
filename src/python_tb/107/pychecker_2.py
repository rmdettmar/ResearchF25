import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 512-bit state register to 0
        self.q_reg = BinaryValue(value=0, n_bits=512)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            load = int(stimulus["load"])
            data = BinaryValue(stimulus["data"], n_bits=512)

            if load:
                # Load new data into register
                self.q_reg = data
            else:
                # Calculate next state for each cell based on Rule 90
                next_state = BinaryValue(0, n_bits=512)

                # Handle first cell (leftmost neighbor is 0)
                next_state[0] = self.q_reg[1]

                # Handle middle cells
                for i in range(1, 511):
                    next_state[i] = (
                        self.q_reg[i - 1].integer ^ self.q_reg[i + 1].integer
                    )

                # Handle last cell (rightmost neighbor is 0)
                next_state[511] = self.q_reg[510]

                # Update state register
                self.q_reg = next_state

            # Add current state to outputs
            stimulus_outputs.append({"q": self.q_reg.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
