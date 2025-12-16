import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state registers needed for this combinational logic circuit
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """
        Process inputs and compute outputs according to 7458 chip logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to boolean values
            p1a = BinaryValue(stimulus["p1a"]).integer
            p1b = BinaryValue(stimulus["p1b"]).integer
            p1c = BinaryValue(stimulus["p1c"]).integer
            p1d = BinaryValue(stimulus["p1d"]).integer
            p1e = BinaryValue(stimulus["p1e"]).integer
            p1f = BinaryValue(stimulus["p1f"]).integer
            p2a = BinaryValue(stimulus["p2a"]).integer
            p2b = BinaryValue(stimulus["p2b"]).integer
            p2c = BinaryValue(stimulus["p2c"]).integer
            p2d = BinaryValue(stimulus["p2d"]).integer

            # Compute p1y: OR of two 3-input AND gates
            and1 = p1a & p1b & p1c
            and2 = p1d & p1e & p1f
            p1y = and1 | and2

            # Compute p2y: OR of two 2-input AND gates
            and3 = p2a & p2b
            and4 = p2c & p2d
            p2y = and3 | and4

            # Convert outputs back to binary strings
            p1y_bin = BinaryValue(value=p1y, n_bits=1).binstr
            p2y_bin = BinaryValue(value=p2y, n_bits=1).binstr

            # Add outputs to result list
            stimulus_outputs.append({"p1y": p1y_bin, "p2y": p2y_bin})

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
