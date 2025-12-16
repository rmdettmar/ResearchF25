import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_bv = BinaryValue(value=stimulus["in"], n_bits=100)

            # Calculate AND output
            out_and = 1
            for i in range(100):
                if in_bv[i] == 0:
                    out_and = 0
                    break

            # Calculate OR output
            out_or = 0
            for i in range(100):
                if in_bv[i] == 1:
                    out_or = 1
                    break

            # Calculate XOR output
            out_xor = 0
            for i in range(100):
                out_xor ^= int(in_bv[i])

            # Create output dictionary for this stimulus
            output = {
                "out_and": str(out_and),
                "out_or": str(out_or),
                "out_xor": str(out_xor),
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
