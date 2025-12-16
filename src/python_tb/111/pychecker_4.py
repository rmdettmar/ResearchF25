import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state"""
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        # Process each input stimulus
        for stimulus in stimulus_dict["input variable"]:
            # Convert input string to BinaryValue
            in_bv = BinaryValue(stimulus["in"], n_bits=1024)
            sel = int(stimulus["sel"], 2)  # Convert binary string to integer

            # Calculate slice indices
            start_idx = sel * 4
            end_idx = start_idx + 4

            # Extract the selected 4-bit slice
            # Convert to BinaryValue to maintain proper bit width
            out_slice = in_bv[start_idx:end_idx]

            # Create output dictionary
            out_dict = {"out": out_slice.binstr}
            stimulus_outputs.append(out_dict)

        # Return formatted output
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
