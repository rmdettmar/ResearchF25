import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input to BinaryValue
            in_bv = BinaryValue(stimulus["in"], n_bits=100)
            in_val = in_bv.binstr

            # Calculate out_both[98:0]
            out_both = ""
            for i in range(99):  # 0 to 98
                out_both = (
                    "1" if in_val[i] == "1" and in_val[i + 1] == "1" else "0"
                ) + out_both
            out_both_bv = BinaryValue(out_both, n_bits=99)

            # Calculate out_any[99:1]
            out_any = ""
            for i in range(99, 1, -1):  # 99 down to 2
                out_any += "1" if in_val[i] == "1" or in_val[i - 1] == "1" else "0"
            out_any_bv = BinaryValue(out_any, n_bits=99)

            # Calculate out_different[99:0]
            out_different = ""
            for i in range(100):  # 0 to 99
                left_neighbor = in_val[(i + 1) % 100]  # Wrap around for MSB
                out_different = (
                    "1" if in_val[i] != left_neighbor else "0"
                ) + out_different
            out_different_bv = BinaryValue(out_different, n_bits=100)

            # Append outputs to result list
            output_list.append(
                {
                    "out_both": out_both_bv.binstr,
                    "out_any": out_any_bv.binstr,
                    "out_different": out_different_bv.binstr,
                }
            )

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
