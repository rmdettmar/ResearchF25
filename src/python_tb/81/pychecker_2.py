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

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process input stimulus and generate output response
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            do_sub = BinaryValue(stimulus["do_sub"]).integer
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer

            # Perform addition or subtraction
            if do_sub:
                self.out = (a - b) & 0xFF  # Constrain to 8 bits
            else:
                self.out = (a + b) & 0xFF  # Constrain to 8 bits

            # Set zero flag
            self.result_is_zero = 1 if self.out == 0 else 0

            # Create output dictionary
            output = {
                "out": format(self.out, "08b"),
                "result_is_zero": format(self.result_is_zero, "01b"),
            }
            stimulus_outputs.append(output)

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
