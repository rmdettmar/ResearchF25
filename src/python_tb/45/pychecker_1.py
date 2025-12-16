import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        pass  # No state needed for combinational logic

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to binary values
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Combine inputs into a 4-bit number
            input_val = (a << 3) | (b << 2) | (c << 1) | d

            # Check if input matches the conditions for logic-1
            # 2 (0010), 7 (0111), 15 (1111)
            output = 1 if input_val in [2, 7, 15] else 0

            # Both SOP and POS forms will give the same result
            out_sop = output
            out_pos = output

            # Convert outputs to binary strings
            result = {"out_sop": str(out_sop), "out_pos": str(out_pos)}
            stimulus_outputs.append(result)

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
