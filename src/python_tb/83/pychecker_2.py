import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No state registers needed as this is combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        # Define the scancode mapping
        scancode_map = {
            0x45: 0,
            0x16: 1,
            0x1E: 2,
            0x26: 3,
            0x25: 4,
            0x2E: 5,
            0x36: 6,
            0x3D: 7,
            0x3E: 8,
            0x46: 9,
        }

        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            code = BinaryValue(stimulus["code"]).integer

            # Check if code exists in mapping
            if code in scancode_map:
                out_val = scancode_map[code]
                valid = 1
            else:
                out_val = 0
                valid = 0

            # Convert outputs to binary strings
            out_bv = BinaryValue(value=out_val, n_bits=4)
            valid_bv = BinaryValue(value=valid, n_bits=1)

            # Add to output list
            stimulus_outputs.append({"out": out_bv.binstr, "valid": valid_bv.binstr})

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
