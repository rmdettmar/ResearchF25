import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize state variables"""
        # No internal state needed as this is combinational logic only
        pass

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and generate outputs"""
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            in_signal = BinaryValue(stimulus["in"])
            state = BinaryValue(stimulus["state"], n_bits=4)

            # Initialize next state
            next_state = BinaryValue(value=0, n_bits=4)

            # State transition logic
            if state.integer == 0b0001:  # State A
                next_state.integer = 0b0001 if in_signal.integer == 0 else 0b0010
            elif state.integer == 0b0010:  # State B
                next_state.integer = 0b0100 if in_signal.integer == 0 else 0b0010
            elif state.integer == 0b0100:  # State C
                next_state.integer = 0b0001 if in_signal.integer == 0 else 0b1000
            elif state.integer == 0b1000:  # State D
                next_state.integer = 0b0100 if in_signal.integer == 0 else 0b0010

            # Output logic - 1 only in state D
            out = "1" if state.integer == 0b1000 else "0"

            # Append outputs for this stimulus
            outputs.append({"next_state": next_state.binstr, "out": out})

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
