import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 4-bit shift register to 0
        self.q_reg = BinaryValue(value=0, n_bits=4)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            areset = BinaryValue(stimulus["areset"]).integer
            load = BinaryValue(stimulus["load"]).integer
            ena = BinaryValue(stimulus["ena"]).integer
            data = BinaryValue(stimulus["data"]).integer

            # Handle asynchronous reset
            if areset:
                self.q_reg = BinaryValue(value=0, n_bits=4)
            else:
                if load:  # Load has priority
                    self.q_reg = BinaryValue(value=data & 0xF, n_bits=4)
                elif ena:  # Shift right if enabled
                    shifted_val = self.q_reg.integer >> 1
                    self.q_reg = BinaryValue(value=shifted_val, n_bits=4)

            # Append current output state
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
