import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        This is a combinational circuit, so no state variables needed
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Implements the combinational logic: q = (b | a) & (c | d)
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer

            # Implement the logic function
            q = ((b | a) & (c | d)) & 0x1

            # Convert output to binary string format
            q_bin = BinaryValue(value=q, n_bits=1, bigEndian=False)

            # Add result to outputs
            stimulus_outputs.append({"q": q_bin.binstr})

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
