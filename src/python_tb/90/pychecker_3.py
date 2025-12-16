import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No state registers needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])
            sel_b1 = BinaryValue(stimulus["sel_b1"])
            sel_b2 = BinaryValue(stimulus["sel_b2"])

            # Calculate out_assign using boolean operations
            out_assign = b if (sel_b1.integer and sel_b2.integer) else a

            # Calculate out_always using if-else (same logic)
            if sel_b1.integer and sel_b2.integer:
                out_always = b
            else:
                out_always = a

            # Add outputs to results
            stimulus_outputs.append(
                {"out_assign": out_assign.binstr, "out_always": out_always.binstr}
            )

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
