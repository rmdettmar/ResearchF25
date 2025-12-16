import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state variables
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to Moore state machine logic
        """
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue
            in_val = BinaryValue(stimulus["in"]).integer
            state_bv = BinaryValue(stimulus["state"])
            state_val = state_bv.integer

            # Calculate next state based on current state and input
            next_state = 0
            if state_val == 0b0001:  # State A
                next_state = 0b0001 if in_val == 0 else 0b0010
            elif state_val == 0b0010:  # State B
                next_state = 0b0100 if in_val == 0 else 0b0010
            elif state_val == 0b0100:  # State C
                next_state = 0b0001 if in_val == 0 else 0b1000
            elif state_val == 0b1000:  # State D
                next_state = 0b0100 if in_val == 0 else 0b0010

            # Calculate output (1 only when in state D)
            out = 1 if state_val == 0b1000 else 0

            # Convert outputs to binary strings
            next_state_bv = BinaryValue(value=next_state, n_bits=4)
            out_bv = BinaryValue(value=out, n_bits=1)

            outputs.append({"next_state": next_state_bv.binstr, "out": out_bv.binstr})

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
