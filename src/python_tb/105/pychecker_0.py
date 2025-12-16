import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize internal state registers"""
        self.prev_in = BinaryValue(value=0, n_bits=8)  # Previous input state

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_bv = BinaryValue(value=stimulus["in"], n_bits=8)

            # Detect positive edges for each bit
            pedge = 0
            for i in range(8):
                # Get previous and current bit values
                prev_bit = int(self.prev_in[i])
                curr_bit = int(in_bv[i])

                # Set output bit if positive edge detected
                if prev_bit == 0 and curr_bit == 1:
                    pedge |= 1 << i

            # Update previous input state
            self.prev_in = in_bv

            # Convert output to binary string
            out_bv = BinaryValue(value=pedge, n_bits=8)
            stimulus_outputs.append({"pedge": out_bv.binstr})

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
