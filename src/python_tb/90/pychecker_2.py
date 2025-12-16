import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational circuit
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        output_list = []

        # Process each set of inputs
        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])
            sel_b1 = BinaryValue(stimulus["sel_b1"])
            sel_b2 = BinaryValue(stimulus["sel_b2"])

            # Implement mux logic
            select_b = sel_b1.integer and sel_b2.integer

            # Both outputs implement the same logic
            out_assign = b.integer if select_b else a.integer
            out_always = b.integer if select_b else a.integer

            # Convert outputs to binary string format
            out_assign_bv = BinaryValue(value=out_assign, n_bits=1)
            out_always_bv = BinaryValue(value=out_always, n_bits=1)

            # Add outputs to result list
            output_list.append(
                {"out_assign": out_assign_bv.binstr, "out_always": out_always_bv.binstr}
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
