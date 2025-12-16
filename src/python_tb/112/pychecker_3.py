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
            # Convert all inputs to BinaryValue
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])
            c = BinaryValue(stimulus["c"])
            d = BinaryValue(stimulus["d"])
            e = BinaryValue(stimulus["e"])
            f = BinaryValue(stimulus["f"])
            g = BinaryValue(stimulus["g"])
            h = BinaryValue(stimulus["h"])
            i = BinaryValue(stimulus["i"])
            sel = BinaryValue(stimulus["sel"])

            # Implement multiplexer logic
            sel_int = sel.integer
            if sel_int == 0:
                out = a.integer
            elif sel_int == 1:
                out = b.integer
            elif sel_int == 2:
                out = c.integer
            elif sel_int == 3:
                out = d.integer
            elif sel_int == 4:
                out = e.integer
            elif sel_int == 5:
                out = f.integer
            elif sel_int == 6:
                out = g.integer
            elif sel_int == 7:
                out = h.integer
            elif sel_int == 8:
                out = i.integer
            else:  # sel 9-15
                out = 0xFFFF  # All 1's for 16 bits

            # Convert output to 16-bit BinaryValue
            out_bv = BinaryValue(value=out, n_bits=16)

            # Add result to outputs list
            stimulus_outputs.append({"out": out_bv.binstr})

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
