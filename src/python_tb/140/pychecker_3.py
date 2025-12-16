import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed as this is combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            c_bv = BinaryValue(stimulus["c"])
            d_bv = BinaryValue(stimulus["d"])

            # Get integer values
            c = c_bv.integer
            d = d_bv.integer

            # Calculate mux_in bits
            mux_in = [0] * 4

            # mux_in[0] (ab=00): 1 when cd=01 or cd=11 or cd=10
            mux_in[0] = 1 if (not c and d) or (c and d) or (c and not d) else 0

            # mux_in[1] (ab=01): always 0
            mux_in[1] = 0

            # mux_in[2] (ab=11): 1 when cd=11
            mux_in[2] = 1 if (c and d) else 0

            # mux_in[3] (ab=10): 1 when cd=00 or cd=11 or cd=10
            mux_in[3] = 1 if (not c and not d) or (c and d) or (c and not d) else 0

            # Convert to 4-bit BinaryValue
            mux_in_bv = BinaryValue(
                value=sum(b << i for i, b in enumerate(mux_in)), n_bits=4
            )

            # Add to outputs
            stimulus_outputs.append({"mux_in": mux_in_bv.binstr})

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
