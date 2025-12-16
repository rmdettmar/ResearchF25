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
            # Convert input strings to BinaryValue objects
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Compute cd value for easier lookup
            cd = (c << 1) | d

            # Initialize mux_in output
            mux_in = 0

            # Calculate mux_in[0] (ab=00 column)
            if cd in [0b01, 0b11, 0b10]:
                mux_in |= 0b0001

            # Calculate mux_in[1] (ab=01 column)
            # All zeros, so nothing to set

            # Calculate mux_in[2] (ab=11 column)
            if cd == 0b11:
                mux_in |= 0b0100

            # Calculate mux_in[3] (ab=10 column)
            if cd in [0b00, 0b11, 0b10]:
                mux_in |= 0b1000

            # Convert to 4-bit binary string
            mux_in_bv = BinaryValue(value=mux_in, n_bits=4)

            # Create output dictionary for this stimulus
            output = {"mux_in": mux_in_bv.binstr}
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
