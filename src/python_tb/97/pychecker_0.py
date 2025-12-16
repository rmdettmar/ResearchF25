import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state register to 000
        self.current_state = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to appropriate format
            reset = int(stimulus["reset"], 2)
            x = int(stimulus["x"], 2)

            # Update state based on reset or state transition
            if reset:
                self.current_state = 0
            else:
                # Implement state transitions based on current state and input x
                if self.current_state == 0b000:
                    self.current_state = 0b000 if x == 0 else 0b001
                elif self.current_state == 0b001:
                    self.current_state = 0b001 if x == 0 else 0b100
                elif self.current_state == 0b010:
                    self.current_state = 0b010 if x == 0 else 0b001
                elif self.current_state == 0b011:
                    self.current_state = 0b001 if x == 0 else 0b010
                elif self.current_state == 0b100:
                    self.current_state = 0b011 if x == 0 else 0b100

            # Determine output based on current state
            z = 1 if self.current_state in [0b011, 0b100] else 0

            # Convert output to binary string
            z_bv = BinaryValue(value=z, n_bits=1)

            stimulus_outputs.append({"z": z_bv.binstr})

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
