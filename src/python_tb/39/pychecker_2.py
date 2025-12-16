import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for combinational circuit
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to BinaryValue
            x_bin = BinaryValue(stimulus["x"], n_bits=4)
            y_bin = BinaryValue(stimulus["y"], n_bits=4)

            # Perform addition
            x_val = x_bin.integer
            y_val = y_bin.integer
            sum_val = x_val + y_val

            # Convert sum to 5-bit BinaryValue
            sum_bin = BinaryValue(value=sum_val, n_bits=5)

            # Add result to outputs
            stimulus_outputs.append({"sum": sum_bin.binstr})

        # Return results in specified format
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
