import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs c and d to generate mux_in[3:0]
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Calculate mux inputs based on c and d
            cd = (c << 1) | d  # Combine c and d into 2-bit value

            mux_in = 0
            # mux_in[0] - for ab=00
            if cd == 0b01 or cd == 0b11 or cd == 0b10:
                mux_in |= 1

            # mux_in[1] - for ab=01
            # All zeros for this case

            # mux_in[2] - for ab=11
            if cd == 0b11:
                mux_in |= 1 << 2

            # mux_in[3] - for ab=10
            if cd == 0b00 or cd == 0b11 or cd == 0b10:
                mux_in |= 1 << 3

            # Convert to 4-bit BinaryValue
            result = BinaryValue(value=mux_in, n_bits=4)

            stimulus_outputs.append({"mux_in": result.binstr})

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
