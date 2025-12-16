import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        This multiplexer has no internal state to initialize
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process each input stimulus and generate corresponding output
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_bv = BinaryValue(value=stimulus["in"], n_bits=1024)
            sel_bv = BinaryValue(value=stimulus["sel"], n_bits=8)

            # Calculate starting bit position
            sel_int = sel_bv.integer
            start_pos = sel_int * 4

            # Extract 4 bits from the input
            # Need to use [start_pos:start_pos+4] to get 4 bits
            out_bv = BinaryValue(value=in_bv.integer >> start_pos, n_bits=4)

            # Add output to results
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
