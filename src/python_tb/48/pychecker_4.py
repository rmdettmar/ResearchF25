import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to BinaryValue
            p1a = BinaryValue(stimulus["p1a"])
            p1b = BinaryValue(stimulus["p1b"])
            p1c = BinaryValue(stimulus["p1c"])
            p1d = BinaryValue(stimulus["p1d"])
            p2a = BinaryValue(stimulus["p2a"])
            p2b = BinaryValue(stimulus["p2b"])
            p2c = BinaryValue(stimulus["p2c"])
            p2d = BinaryValue(stimulus["p2d"])

            # Calculate NAND outputs
            p1y = (
                "0"
                if (p1a.integer and p1b.integer and p1c.integer and p1d.integer)
                else "1"
            )
            p2y = (
                "0"
                if (p2a.integer and p2b.integer and p2c.integer and p2d.integer)
                else "1"
            )

            # Create output dictionary for this stimulus
            output = {"p1y": p1y, "p2y": p2y}
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
