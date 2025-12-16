import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state register
        self.q_reg = BinaryValue(value=0, n_bits=4)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []
        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            areset = int(stimulus["areset"], 2)
            load = int(stimulus["load"], 2)
            ena = int(stimulus["ena"], 2)
            data = BinaryValue(value=int(stimulus["data"], 2), n_bits=4)

            # Handle asynchronous reset
            if areset:
                self.q_reg = BinaryValue(value=0, n_bits=4)
            else:
                if load:
                    # Load data into register
                    self.q_reg = data
                elif ena:
                    # Right shift (q[3] becomes 0)
                    shifted_val = (self.q_reg.integer >> 1) & 0xF
                    self.q_reg = BinaryValue(value=shifted_val, n_bits=4)

            # Append current output to results
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
