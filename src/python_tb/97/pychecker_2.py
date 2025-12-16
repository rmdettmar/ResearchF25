import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state register to 000
        self.state = BinaryValue(value=0, n_bits=3)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signals
            reset = int(stimulus["reset"], 2)
            x = int(stimulus["x"], 2)

            # Update state based on reset or state transition
            if reset:
                self.state = BinaryValue(value=0, n_bits=3)
            else:
                current_state = self.state.integer
                # Determine next state based on current state and input x
                if current_state == 0:  # 000
                    next_state = 1 if x else 0
                elif current_state == 1:  # 001
                    next_state = 4 if x else 1
                elif current_state == 2:  # 010
                    next_state = 1 if x else 2
                elif current_state == 3:  # 011
                    next_state = 2 if x else 1
                elif current_state == 4:  # 100
                    next_state = 4 if x else 3
                else:
                    next_state = 0  # Invalid state goes to 000

                self.state = BinaryValue(value=next_state, n_bits=3)

            # Determine output z based on current state
            z = 1 if self.state.integer in [3, 4] else 0

            # Add output to results
            stimulus_outputs.append({"z": format(z, "b")})

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
