import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 3-bit state register to 000
        self.state = BinaryValue(value=0, n_bits=3)
        self.z = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)
            x = int(stimulus["x"], 2)

            if reset:
                # Synchronous reset to state 000
                self.state = BinaryValue(value=0, n_bits=3)
                self.z = 0
            else:
                current_state = self.state.integer
                # Implement state transitions based on current state and input x
                if current_state == 0:  # 000
                    self.state = BinaryValue(value=1 if x else 0, n_bits=3)
                    self.z = 0
                elif current_state == 1:  # 001
                    self.state = BinaryValue(value=4 if x else 1, n_bits=3)
                    self.z = 0
                elif current_state == 2:  # 010
                    self.state = BinaryValue(value=1 if x else 2, n_bits=3)
                    self.z = 0
                elif current_state == 3:  # 011
                    self.state = BinaryValue(value=2 if x else 1, n_bits=3)
                    self.z = 1
                elif current_state == 4:  # 100
                    self.state = BinaryValue(value=4 if x else 3, n_bits=3)
                    self.z = 1

            stimulus_outputs.append({"z": format(self.z, "b")})

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
