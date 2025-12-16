import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Combine inputs into 4-bit number
            input_val = (a << 3) | (b << 2) | (c << 1) | d

            # Calculate out_sop (1 for 2,7,15)
            out_sop = 1 if input_val in [2, 7, 15] else 0

            # Calculate out_pos (0 for 0,1,4,5,6,9,10,13,14)
            out_pos = 0 if input_val in [0, 1, 4, 5, 6, 9, 10, 13, 14] else 1

            # Create output dictionary for this stimulus
            output = {
                "out_sop": BinaryValue(value=out_sop, n_bits=1).binstr,
                "out_pos": BinaryValue(value=out_pos, n_bits=1).binstr,
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
