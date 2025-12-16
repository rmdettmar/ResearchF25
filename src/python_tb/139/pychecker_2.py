import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        # Process each set of inputs
        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            in1_bv = BinaryValue(stimulus["in1"])
            in2_bv = BinaryValue(stimulus["in2"])
            in3_bv = BinaryValue(stimulus["in3"])

            # Get integer values
            in1 = in1_bv.integer
            in2 = in2_bv.integer
            in3 = in3_bv.integer

            # Implement XNOR followed by XOR
            xnor_result = ~(in1 ^ in2) & 1  # XNOR of in1 and in2
            out = (xnor_result ^ in3) & 1  # XOR with in3

            # Convert result to BinaryValue
            out_bv = BinaryValue(value=out, n_bits=1)

            # Add to outputs
            stimulus_outputs.append({"out": out_bv.binstr})

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
