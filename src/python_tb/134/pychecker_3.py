import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            a = BinaryValue(stimulus["a"]).integer
            b = BinaryValue(stimulus["b"]).integer
            c = BinaryValue(stimulus["c"]).integer
            d = BinaryValue(stimulus["d"]).integer
            e = BinaryValue(stimulus["e"]).integer
            f = BinaryValue(stimulus["f"]).integer

            # Concatenate all inputs and add two '1' bits at LSB
            # {a,b,c,d,e,f,2'b11}
            concat = (
                (a << 27)
                | (b << 22)
                | (c << 17)
                | (d << 12)
                | (e << 7)
                | (f << 2)
                | 0b11
            )

            # Split into 8-bit outputs
            w = (concat >> 24) & 0xFF
            x = (concat >> 16) & 0xFF
            y = (concat >> 8) & 0xFF
            z = concat & 0xFF

            # Convert to binary strings with proper width
            w_bv = BinaryValue(value=w, n_bits=8)
            x_bv = BinaryValue(value=x, n_bits=8)
            y_bv = BinaryValue(value=y, n_bits=8)
            z_bv = BinaryValue(value=z, n_bits=8)

            output = {
                "w": w_bv.binstr,
                "x": x_bv.binstr,
                "y": y_bv.binstr,
                "z": z_bv.binstr,
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
