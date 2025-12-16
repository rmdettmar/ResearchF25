import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state variables needed as this is combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Calculate cd value (2-bit)
            cd = (c << 1) | d

            # Calculate mux_in values based on K-map
            mux_in = 0

            # mux_in[0] (ab=00): 0,1,1,1 pattern
            if cd == 0:
                mux_in_0 = 0
            else:
                mux_in_0 = 1

            # mux_in[1] (ab=01): all 0s
            mux_in_1 = 0

            # mux_in[2] (ab=11): 0,0,1,0 pattern
            if cd == 2:
                mux_in_2 = 1
            else:
                mux_in_2 = 0

            # mux_in[3] (ab=10): 1,0,1,1 pattern
            if cd == 0:
                mux_in_3 = 1
            elif cd == 1:
                mux_in_3 = 0
            else:
                mux_in_3 = 1

            # Combine all outputs
            mux_in = (mux_in_3 << 3) | (mux_in_2 << 2) | (mux_in_1 << 1) | mux_in_0

            # Convert to 4-bit BinaryValue
            mux_in_bv = BinaryValue(value=mux_in, n_bits=4)

            stimulus_outputs.append({"mux_in": mux_in_bv.binstr})

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
