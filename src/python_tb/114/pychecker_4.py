import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables
        """
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to state machine logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to BinaryValue
            in_signal = BinaryValue(stimulus["in"])
            state = BinaryValue(stimulus["state"], n_bits=4)

            # Initialize next state
            next_state = BinaryValue(value=0, n_bits=4)

            # State transition logic
            if state.binstr == "0001":  # State A
                next_state = BinaryValue(
                    "0001" if in_signal.integer == 0 else "0010", n_bits=4
                )
            elif state.binstr == "0010":  # State B
                next_state = BinaryValue(
                    "0100" if in_signal.integer == 0 else "0010", n_bits=4
                )
            elif state.binstr == "0100":  # State C
                next_state = BinaryValue(
                    "0001" if in_signal.integer == 0 else "1000", n_bits=4
                )
            elif state.binstr == "1000":  # State D
                next_state = BinaryValue(
                    "0100" if in_signal.integer == 0 else "0010", n_bits=4
                )

            # Output logic - 1 only in state D
            out = 1 if state.binstr == "1000" else 0

            # Add outputs to results
            stimulus_outputs.append({"next_state": next_state.binstr, "out": str(out)})

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
