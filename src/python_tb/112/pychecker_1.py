import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # This is a combinational logic module, no state needed
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            a = BinaryValue(stimulus["a"], n_bits=16).integer
            b = BinaryValue(stimulus["b"], n_bits=16).integer
            c = BinaryValue(stimulus["c"], n_bits=16).integer
            d = BinaryValue(stimulus["d"], n_bits=16).integer
            e = BinaryValue(stimulus["e"], n_bits=16).integer
            f = BinaryValue(stimulus["f"], n_bits=16).integer
            g = BinaryValue(stimulus["g"], n_bits=16).integer
            h = BinaryValue(stimulus["h"], n_bits=16).integer
            i = BinaryValue(stimulus["i"], n_bits=16).integer
            sel = BinaryValue(stimulus["sel"], n_bits=4).integer

            # Implement multiplexer logic
            if sel == 0:
                out = a
            elif sel == 1:
                out = b
            elif sel == 2:
                out = c
            elif sel == 3:
                out = d
            elif sel == 4:
                out = e
            elif sel == 5:
                out = f
            elif sel == 6:
                out = g
            elif sel == 7:
                out = h
            elif sel == 8:
                out = i
            else:  # sel >= 9
                out = 0xFFFF

            # Convert output to BinaryValue for consistent format
            out_bv = BinaryValue(value=out, n_bits=16)
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
