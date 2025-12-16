import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert all inputs to BinaryValue
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer
            e = BinaryValue(stimulus["e"]).integer
            f = BinaryValue(stimulus["f"]).integer

            # Concatenate all inputs and add two '1' bits at LSB
            # Shift each value to its proper position
            concat = (
                (a << 27)
                | (b << 22)
                | (c << 17)
                | (d << 12)
                | (e << 7)
                | (f << 2)
                | 0b11
            )

            # Extract 8-bit segments for outputs
            w_val = (concat >> 24) & 0xFF
            x_val = (concat >> 16) & 0xFF
            y_val = (concat >> 8) & 0xFF
            z_val = concat & 0xFF

            # Convert to 8-bit BinaryValue objects
            w = BinaryValue(value=w_val, n_bits=8).binstr
            x = BinaryValue(value=x_val, n_bits=8).binstr
            y = BinaryValue(value=y_val, n_bits=8).binstr
            z = BinaryValue(value=z_val, n_bits=8).binstr

            # Add to output list
            stimulus_outputs.append({"w": w, "x": x, "y": y, "z": z})

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
