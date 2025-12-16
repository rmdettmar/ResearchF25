import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state registers
        self.p = 0
        self.q = 0
        self.prev_clock = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            clock = BinaryValue(stimulus["clock"]).integer
            a = BinaryValue(stimulus["a"]).integer

            # Detect clock edges
            rising_edge = (self.prev_clock == 0) and (clock == 1)
            falling_edge = (self.prev_clock == 1) and (clock == 0)

            # Update states based on clock edges
            if rising_edge:
                self.p = a
            if falling_edge:
                self.q = self.p

            # Store current clock for next iteration
            self.prev_clock = clock

            # Format outputs as binary strings
            p_bv = BinaryValue(value=self.p, n_bits=1)
            q_bv = BinaryValue(value=self.q, n_bits=1)

            # Add current outputs to results
            stimulus_outputs.append({"p": p_bv.binstr, "q": q_bv.binstr})

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
