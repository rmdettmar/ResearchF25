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
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input to BinaryValue
            in_bv = BinaryValue(value=stimulus["in"], n_bits=100)
            in_str = in_bv.binstr

            # Calculate out_both[98:0]
            out_both = ""
            for i in range(99):
                # Check if current bit and left neighbor are both 1
                out_both = (
                    "1" if in_str[98 - i] == "1" and in_str[99 - i] == "1" else "0"
                ) + out_both
            out_both_bv = BinaryValue(value=out_both, n_bits=99)

            # Calculate out_any[99:1]
            out_any = ""
            for i in range(99, 0, -1):
                # Check if current bit or right neighbor are 1
                out_any += "1" if in_str[i] == "1" or in_str[i - 1] == "1" else "0"
            out_any_bv = BinaryValue(value=out_any, n_bits=99)

            # Calculate out_different[99:0]
            out_different = ""
            for i in range(100):
                # Get left neighbor (wrapping around for MSB)
                left_neighbor = in_str[0] if i == 99 else in_str[i + 1]
                # Check if current bit is different from left neighbor
                out_different = (
                    "1" if in_str[i] != left_neighbor else "0"
                ) + out_different
            out_different_bv = BinaryValue(value=out_different, n_bits=100)

            # Append outputs to results
            stimulus_outputs.append(
                {
                    "out_both": out_both_bv.binstr,
                    "out_any": out_any_bv.binstr,
                    "out_different": out_different_bv.binstr,
                }
            )

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
