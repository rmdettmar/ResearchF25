import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        # Process each input stimulus
        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_bv = BinaryValue(stimulus["in"])
            in_val = in_bv.integer

            # Calculate AND output - all bits must be 1
            out_and = 1 if in_val == 0xF else 0

            # Calculate OR output - any bit being 1
            out_or = 1 if in_val > 0 else 0

            # Calculate XOR output - count number of 1s
            out_xor = 0
            temp = in_val
            while temp:
                out_xor ^= temp & 1
                temp >>= 1

            # Add outputs to result list
            stimulus_outputs.append(
                {
                    "out_and": str(out_and),
                    "out_or": str(out_or),
                    "out_xor": str(out_xor),
                }
            )

        # Return formatted output dictionary
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
