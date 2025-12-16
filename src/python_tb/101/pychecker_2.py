import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        No state registers needed as this is combinational logic
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to BinaryValue
            in_sig = BinaryValue(stimulus["in"])
            state = BinaryValue(stimulus["state"], n_bits=2)

            # State transition logic
            if state.integer == 0:  # State A
                next_state = 0 if in_sig.integer == 0 else 1  # A->A or A->B
            elif state.integer == 1:  # State B
                next_state = 2 if in_sig.integer == 0 else 1  # B->C or B->B
            elif state.integer == 2:  # State C
                next_state = 0 if in_sig.integer == 0 else 3  # C->A or C->D
            else:  # State D
                next_state = 2 if in_sig.integer == 0 else 1  # D->C or D->B

            # Output logic (Moore machine)
            out = 1 if state.integer == 3 else 0  # Only state D outputs 1

            # Convert outputs to proper format
            next_state_bv = BinaryValue(value=next_state, n_bits=2)
            out_bv = BinaryValue(value=out, n_bits=1)

            stimulus_outputs.append(
                {"next_state": next_state_bv.binstr, "out": out_bv.binstr}
            )

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
