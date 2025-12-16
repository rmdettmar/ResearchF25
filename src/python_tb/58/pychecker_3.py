import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state variables
        """
        pass

    def module_a(self, x: int, y: int) -> int:
        """
        Implement module A logic: z = (x^y) & x
        """
        return (x ^ y) & x

    def module_b(self, x: int, y: int) -> int:
        """
        Implement module B logic: z = ~(x^y)
        """
        return int(not (x ^ y))

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to the circuit logic
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary strings to integers
            x = int(stimulus["x"], 2)
            y = int(stimulus["y"], 2)

            # Calculate outputs of A1, A2, B1, B2
            z_a1 = self.module_a(x, y)
            z_a2 = self.module_a(x, y)
            z_b1 = self.module_b(x, y)
            z_b2 = self.module_b(x, y)

            # Calculate OR and AND outputs
            or_out = z_a1 | z_b1
            and_out = z_a2 & z_b2

            # Calculate final XOR output
            z = or_out ^ and_out

            # Convert output to binary string
            z_bin = format(z, "b")

            outputs.append({"z": z_bin})

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
