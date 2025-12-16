import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state
        """
        self.out = BinaryValue(value=0, n_bits=8)
        self.result_is_zero = BinaryValue(value=0, n_bits=1)

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            do_sub = BinaryValue(stimulus["do_sub"])
            a = BinaryValue(stimulus["a"], n_bits=8)
            b = BinaryValue(stimulus["b"], n_bits=8)

            # Perform addition or subtraction
            if do_sub.integer == 0:
                result = (a.integer + b.integer) & 0xFF  # Add with 8-bit wrap
            else:
                result = (a.integer - b.integer) & 0xFF  # Subtract with 8-bit wrap

            # Update outputs
            self.out = BinaryValue(value=result, n_bits=8)
            self.result_is_zero = (
                BinaryValue(value=1, n_bits=1)
                if result == 0
                else BinaryValue(value=0, n_bits=1)
            )

            # Add results to output list
            stimulus_outputs.append(
                {"out": self.out.binstr, "result_is_zero": self.result_is_zero.binstr}
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
