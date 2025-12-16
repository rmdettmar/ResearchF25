import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def find_first_one(self, in_val: str) -> int:
        # Convert input string to BinaryValue
        bv = BinaryValue(in_val)
        # Get binary string representation
        bin_str = bv.binstr
        # Scan from LSB (right) to MSB (left)
        for i in range(8):
            if bin_str[-1 - i] == "1":
                return i
        return 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        # Process each input stimulus
        for stimulus in stimulus_dict["input variable"]:
            in_val = stimulus["in"]
            # Find position of first '1' bit
            pos = self.find_first_one(in_val)
            # Create output dictionary
            output = {"pos": format(pos, "03b")}
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
