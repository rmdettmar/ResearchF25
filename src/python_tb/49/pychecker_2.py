import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for combinational population count
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Count number of 1's in the input vector
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_signal = BinaryValue(stimulus["in"])

            # Count number of 1's in the binary representation
            ones_count = bin(in_signal.integer).count("1")

            # Convert count to 8-bit BinaryValue and get binary string
            out_signal = BinaryValue(value=ones_count, n_bits=8)

            # Add the output to results
            stimulus_outputs.append({"out": out_signal.binstr})

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
