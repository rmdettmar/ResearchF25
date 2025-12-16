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
            # Convert input strings to BinaryValue
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])
            c = BinaryValue(stimulus["c"])
            d = BinaryValue(stimulus["d"])

            # Implement the combinational logic
            wire1 = a.integer & b.integer  # First AND gate
            wire2 = c.integer & d.integer  # Second AND gate
            out = wire1 | wire2  # OR gate
            out_n = ~out & 0x1  # NOT gate

            # Create output dictionary for this stimulus
            output = {
                "out": BinaryValue(value=out, n_bits=1).binstr,
                "out_n": BinaryValue(value=out_n, n_bits=1).binstr,
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
