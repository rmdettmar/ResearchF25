import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.p = 0  # p starts at 0
        self.q = 0  # q starts at x but we'll use 0
        self.prev_clk = 0  # Track clock transitions

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue for proper handling
            clock = BinaryValue(stimulus["clock"]).integer
            a = BinaryValue(stimulus["a"]).integer

            # Detect positive clock edge
            if clock == 1 and self.prev_clk == 0:
                # Update state on positive clock edge
                old_p = self.p
                if a == 1:
                    self.p = 1
                else:
                    self.p = 0
                    self.q = old_p

            # Store current clock for next edge detection
            self.prev_clk = clock

            # Format outputs as binary strings
            p_bv = BinaryValue(value=self.p, n_bits=1)
            q_bv = BinaryValue(value=self.q, n_bits=1)

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
