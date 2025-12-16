import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for this combinational logic
        pass

    def concatenate_inputs(
        self, a: str, b: str, c: str, d: str, e: str, f: str
    ) -> BinaryValue:
        # Convert input strings to BinaryValue objects
        a_bv = BinaryValue(a, n_bits=5)
        b_bv = BinaryValue(b, n_bits=5)
        c_bv = BinaryValue(c, n_bits=5)
        d_bv = BinaryValue(d, n_bits=5)
        e_bv = BinaryValue(e, n_bits=5)
        f_bv = BinaryValue(f, n_bits=5)

        # Concatenate all inputs with two '1' bits at LSB
        # Total width: 30 (inputs) + 2 (ones) = 32 bits
        concat_val = (
            (f_bv.integer << 27)
            | (e_bv.integer << 22)
            | (d_bv.integer << 17)
            | (c_bv.integer << 12)
            | (b_bv.integer << 7)
            | (a_bv.integer << 2)
            | 0b11
        )

        return BinaryValue(value=concat_val, n_bits=32)

    def load(self, stimulus_dict: Dict[str, any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract input signals
            a = stimulus["a"]
            b = stimulus["b"]
            c = stimulus["c"]
            d = stimulus["d"]
            e = stimulus["e"]
            f = stimulus["f"]

            # Concatenate inputs and add two '1' bits
            concat_result = self.concatenate_inputs(a, b, c, d, e, f)

            # Split into 8-bit outputs
            w = BinaryValue(value=concat_result.integer >> 24, n_bits=8).binstr
            x = BinaryValue(value=(concat_result.integer >> 16) & 0xFF, n_bits=8).binstr
            y = BinaryValue(value=(concat_result.integer >> 8) & 0xFF, n_bits=8).binstr
            z = BinaryValue(value=concat_result.integer & 0xFF, n_bits=8).binstr

            output_list.append({"w": w, "x": x, "y": y, "z": z})

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
