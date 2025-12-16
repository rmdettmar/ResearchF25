import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to OFF (0)
        self.current_state = 0
        self.OUT_STATE = {"OFF": 0, "ON": 1}

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus["reset"]).integer
            j = BinaryValue(stimulus["j"]).integer
            k = BinaryValue(stimulus["k"]).integer

            # State update logic
            if reset:
                self.current_state = self.OUT_STATE["OFF"]
            else:
                if self.current_state == self.OUT_STATE["OFF"]:
                    if j:
                        self.current_state = self.OUT_STATE["ON"]
                else:  # current_state == ON
                    if k:
                        self.current_state = self.OUT_STATE["OFF"]

            # Output is same as current state (Moore machine)
            out = BinaryValue(value=self.current_state, n_bits=1)
            stimulus_outputs.append({"out": out.binstr})

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
