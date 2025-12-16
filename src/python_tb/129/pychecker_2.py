import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 8-bit register q to 0
        self.q_reg = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            d = BinaryValue(stimulus["d"], n_bits=8)
            areset = BinaryValue(stimulus["areset"], n_bits=1)

            # Handle asynchronous reset
            if areset.integer == 1:
                self.q_reg = BinaryValue(value=0, n_bits=8)
            else:
                # On positive clock edge, update q with d
                self.q_reg = BinaryValue(value=d.integer, n_bits=8)

            # Add current output to stimulus_outputs
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
