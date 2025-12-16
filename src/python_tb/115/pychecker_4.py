import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize min register
        self.min_reg = BinaryValue(value=0, n_bits=8)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a_bv = BinaryValue(value=stimulus["a"], n_bits=8)
            b_bv = BinaryValue(value=stimulus["b"], n_bits=8)
            c_bv = BinaryValue(value=stimulus["c"], n_bits=8)
            d_bv = BinaryValue(value=stimulus["d"], n_bits=8)

            # Convert to integers for comparison
            a = a_bv.integer
            b = b_bv.integer
            c = c_bv.integer
            d = d_bv.integer

            # Find minimum value
            min_val = min(a, b, c, d)

            # Update min register
            self.min_reg = BinaryValue(value=min_val, n_bits=8)

            # Add to outputs
            stimulus_outputs.append({"min": self.min_reg.binstr})

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
