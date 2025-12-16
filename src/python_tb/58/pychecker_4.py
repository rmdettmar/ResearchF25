import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def module_a(self, x: int, y: int) -> int:
        # z = (x^y) & x
        return (x ^ y) & x

    def module_b(self, x: int, y: int) -> int:
        # z = (~x & ~y) | (x & y)
        return (~x & ~y & 1) | (x & y)

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary strings to integers
            x = int(stimulus["x"], 2)
            y = int(stimulus["y"], 2)

            # Calculate outputs of A modules
            a1_out = self.module_a(x, y)
            a2_out = self.module_a(x, y)

            # Calculate outputs of B modules
            b1_out = self.module_b(x, y)
            b2_out = self.module_b(x, y)

            # Combine outputs according to top level structure
            or_out = a1_out | b1_out
            and_out = a2_out & b2_out

            # Final XOR
            z = or_out ^ and_out

            # Convert result back to binary string
            outputs.append({"z": format(z & 1, "b")})

        return {"scenario": stimulus_dict["scenario"], "output variable": outputs}


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
