import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.out = 0
        self.result_is_zero = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process input stimulus and generate output
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to integers
            do_sub = BinaryValue(stimulus["do_sub"]).integer
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer

            # Perform add/subtract operation
            if do_sub == 0:
                self.out = (a + b) & 0xFF  # 8-bit addition
            else:
                self.out = (a - b) & 0xFF  # 8-bit subtraction

            # Check if result is zero
            self.result_is_zero = 1 if self.out == 0 else 0

            # Convert results to binary strings
            out_bv = BinaryValue(value=self.out, n_bits=8)
            result_is_zero_bv = BinaryValue(value=self.result_is_zero, n_bits=1)

            # Add to output list
            stimulus_outputs.append(
                {"out": out_bv.binstr, "result_is_zero": result_is_zero_bv.binstr}
            )

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
