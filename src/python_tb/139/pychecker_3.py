import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            in1_bv = BinaryValue(stimulus["in1"])
            in2_bv = BinaryValue(stimulus["in2"])
            in3_bv = BinaryValue(stimulus["in3"])

            # Calculate XNOR of in1 and in2
            xnor_result = not (in1_bv.integer ^ in2_bv.integer)

            # Calculate XOR of XNOR result and in3
            out = xnor_result ^ in3_bv.integer

            # Convert to BinaryValue for consistent output format
            out_bv = BinaryValue(value=out, n_bits=1)

            # Add to output list
            stimulus_outputs.append({"out": out_bv.binstr})

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
