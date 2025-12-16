import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # No internal state needed for combinational logic
        pass

    def _compute_and(self, in_bits: BinaryValue) -> int:
        # Compute AND of all bits
        result = 1
        for i in range(100):
            if in_bits[i] == 0:
                result = 0
                break
        return result

    def _compute_or(self, in_bits: BinaryValue) -> int:
        # Compute OR of all bits
        result = 0
        for i in range(100):
            if in_bits[i] == 1:
                result = 1
                break
        return result

    def _compute_xor(self, in_bits: BinaryValue) -> int:
        # Compute XOR of all bits
        result = 0
        for i in range(100):
            result ^= in_bits[i]
        return result

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input binary string to BinaryValue
            in_bits = BinaryValue(stimulus["in"], n_bits=100)

            # Compute all outputs
            out_and = self._compute_and(in_bits)
            out_or = self._compute_or(in_bits)
            out_xor = self._compute_xor(in_bits)

            # Format output as dictionary
            output = {
                "out_and": BinaryValue(value=out_and, n_bits=1).binstr,
                "out_or": BinaryValue(value=out_or, n_bits=1).binstr,
                "out_xor": BinaryValue(value=out_xor, n_bits=1).binstr,
            }
            outputs.append(output)

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
