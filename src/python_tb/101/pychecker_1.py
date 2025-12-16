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
            # Convert inputs to BinaryValue
            in_val = BinaryValue(stimulus["in"])
            state = BinaryValue(stimulus["state"], n_bits=2)

            # Calculate next state based on current state and input
            if state.integer == 0:  # State A
                next_state = 0 if in_val.integer == 0 else 1
            elif state.integer == 1:  # State B
                next_state = 2 if in_val.integer == 0 else 1
            elif state.integer == 2:  # State C
                next_state = 0 if in_val.integer == 0 else 3
            else:  # State D
                next_state = 2 if in_val.integer == 0 else 1

            # Calculate output (1 only in state D)
            out = 1 if state.integer == 3 else 0

            # Convert next_state to binary string
            next_state_bv = BinaryValue(value=next_state, n_bits=2)

            # Create output dictionary for this stimulus
            output = {"next_state": next_state_bv.binstr, "out": str(out)}
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
