import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state flip-flop
        self.state = BinaryValue("0")

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            clk = BinaryValue(stimulus["clk"])
            a = BinaryValue(stimulus["a"])
            b = BinaryValue(stimulus["b"])

            # Update state on positive clock edge
            if clk.integer == 1:
                if a.integer == 1 and b.integer == 1:
                    # Toggle state when a=1 and b=1
                    self.state = BinaryValue(value=not self.state.integer, n_bits=1)

            # Calculate output q
            if self.state.integer == 0:
                # When state is 0
                if (a.integer == 0 and b.integer == 1) or (
                    a.integer == 1 and b.integer == 0
                ):
                    q = BinaryValue("1")
                else:
                    q = BinaryValue("0")
            else:
                # When state is 1
                if (a.integer == 1 and b.integer == 0) or (
                    a.integer == 0 and b.integer == 1
                ):
                    q = BinaryValue("0")
                else:
                    q = BinaryValue("1")

            # Append outputs to results
            stimulus_outputs.append({"q": q.binstr, "state": self.state.binstr})

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
