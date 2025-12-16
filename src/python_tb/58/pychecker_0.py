import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        pass

    def module_a(self, x: int, y: int) -> int:
        """Implement module A: z = (x^y) & x"""
        return (x ^ y) & x

    def module_b(self, x: int, y: int) -> int:
        """Implement module B: z = ~(x | y)"""
        return int(not (x or y))

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to BinaryValue objects
            x_bv = BinaryValue(stimulus["x"])
            y_bv = BinaryValue(stimulus["y"])

            # Convert to integers for computation
            x = x_bv.integer
            y = y_bv.integer

            # Calculate outputs of all submodules
            a1_out = self.module_a(x, y)
            b1_out = self.module_b(x, y)
            a2_out = self.module_a(x, y)
            b2_out = self.module_b(x, y)

            # Combine through gates
            or_out = a1_out | b1_out
            and_out = a2_out & b2_out
            z = or_out ^ and_out

            # Convert output to binary string
            z_bv = BinaryValue(value=z, n_bits=1)
            outputs.append({"z": z_bv.binstr})

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
