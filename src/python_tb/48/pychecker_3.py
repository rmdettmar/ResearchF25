import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert string inputs to BinaryValue objects
            p1a = BinaryValue(stimulus["p1a"]).integer
            p1b = BinaryValue(stimulus["p1b"]).integer
            p1c = BinaryValue(stimulus["p1c"]).integer
            p1d = BinaryValue(stimulus["p1d"]).integer
            p2a = BinaryValue(stimulus["p2a"]).integer
            p2b = BinaryValue(stimulus["p2b"]).integer
            p2c = BinaryValue(stimulus["p2c"]).integer
            p2d = BinaryValue(stimulus["p2d"]).integer

            # Compute NAND gate outputs
            p1y = 0 if (p1a and p1b and p1c and p1d) else 1
            p2y = 0 if (p2a and p2b and p2c and p2d) else 1

            # Convert outputs to binary string format
            output_dict = {
                "p1y": BinaryValue(p1y, n_bits=1).binstr,
                "p2y": BinaryValue(p2y, n_bits=1).binstr,
            }
            stimulus_outputs.append(output_dict)

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
