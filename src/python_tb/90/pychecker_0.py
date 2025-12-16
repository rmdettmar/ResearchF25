import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state registers needed for this combinational circuit
        """
        pass

    def _compute_mux(self, a: int, b: int, sel_b1: int, sel_b2: int) -> int:
        """
        Helper method to compute mux output
        Returns b if both sel_b1 and sel_b2 are true, otherwise returns a
        """
        return b if (sel_b1 and sel_b2) else a

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to mux logic
        """
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a_bv = BinaryValue(stimulus["a"])
            b_bv = BinaryValue(stimulus["b"])
            sel_b1_bv = BinaryValue(stimulus["sel_b1"])
            sel_b2_bv = BinaryValue(stimulus["sel_b2"])

            # Get integer values
            a = a_bv.integer
            b = b_bv.integer
            sel_b1 = sel_b1_bv.integer
            sel_b2 = sel_b2_bv.integer

            # Compute output
            out = self._compute_mux(a, b, sel_b1, sel_b2)

            # Convert output to binary string
            out_bv = BinaryValue(value=out, n_bits=1)

            # Add to output list
            output_list.append(
                {"out_assign": out_bv.binstr, "out_always": out_bv.binstr}
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
