import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize output register
        self.out_reg = BinaryValue(value=0, n_bits=100)

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input value and convert to BinaryValue
            in_val = BinaryValue(value=stimulus["in"], n_bits=100)

            # Reverse all bits
            in_str = in_val.binstr
            reversed_str = in_str[::-1]

            # Store in output register
            self.out_reg = BinaryValue(
                value=reversed_str,
                n_bits=100,
                binaryRepresentation=BinaryValue.UNSIGNED,
            )

            # Append to outputs
            stimulus_outputs.append({"out": self.out_reg.binstr})

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
