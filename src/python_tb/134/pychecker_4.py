import json
from typing import Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No internal state needed for this combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to RTL specification
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])
            c = BinaryValue(stimulus["c"])
            d = BinaryValue(stimulus["d"])
            e = BinaryValue(stimulus["e"])
            f = BinaryValue(stimulus["f"])

            # Concatenate all inputs and add two '1' bits
            # Convert to integer for easier manipulation
            concat = (
                (f.integer << 27)
                | (e.integer << 22)
                | (d.integer << 17)
                | (c.integer << 12)
                | (b.integer << 7)
                | (a.integer << 2)
                | 0b11
            )

            # Create output vectors by slicing
            w = (concat >> 24) & 0xFF
            x = (concat >> 16) & 0xFF
            y = (concat >> 8) & 0xFF
            z = concat & 0xFF

            # Convert to binary strings
            w_bv = BinaryValue(value=w, n_bits=8)
            x_bv = BinaryValue(value=x, n_bits=8)
            y_bv = BinaryValue(value=y, n_bits=8)
            z_bv = BinaryValue(value=z, n_bits=8)

            output_dict = {
                "w": w_bv.binstr,
                "x": x_bv.binstr,
                "y": y_bv.binstr,
                "z": z_bv.binstr,
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
