import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state variables needed for combinational circuit
        # Create lookup table for input-output mapping
        self.lut = {
            0: 0x1232,
            1: 0xAEE0,
            2: 0x27D4,
            3: 0x5A0E,
            4: 0x2066,
            5: 0x64CE,
            6: 0xC526,
            7: 0x2F19,
        }

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            a_bv = BinaryValue(stimulus["a"])
            # Get integer value
            a_val = a_bv.integer

            # Look up the output value
            q_val = self.lut[a_val]

            # Convert to 16-bit binary string
            q_bv = BinaryValue(value=q_val, n_bits=16)

            # Add to outputs
            stimulus_outputs.append({"q": q_bv.binstr})

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
