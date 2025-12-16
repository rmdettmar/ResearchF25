import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers.
        For this combinational logic, no state registers are needed.
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and generate outputs according to mux logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            sel_b1 = BinaryValue(stimulus["sel_b1"]).integer
            sel_b2 = BinaryValue(stimulus["sel_b2"]).integer

            # Compute outputs
            if sel_b1 and sel_b2:
                out_assign = b
                out_always = b
            else:
                out_assign = a
                out_always = a

            # Convert outputs back to binary strings
            out_assign_bv = BinaryValue(value=out_assign, n_bits=1)
            out_always_bv = BinaryValue(value=out_always, n_bits=1)

            # Add outputs to result list
            output = {
                "out_assign": out_assign_bv.binstr,
                "out_always": out_always_bv.binstr,
            }
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
