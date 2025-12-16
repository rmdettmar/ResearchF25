import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.current_state = BinaryValue("0000000001", n_bits=10)  # S0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signal
            in_signal = BinaryValue(stimulus["in"])
            state = BinaryValue(stimulus["state"], n_bits=10)

            # Calculate next state based on current state and input
            next_state = BinaryValue("0" * 10, n_bits=10)

            # State transition logic
            if state[0]:  # S0
                next_state[0 if not in_signal.integer else 1] = 1
            elif state[1]:  # S1
                next_state[0 if not in_signal.integer else 2] = 1
            elif state[2]:  # S2
                next_state[0 if not in_signal.integer else 3] = 1
            elif state[3]:  # S3
                next_state[0 if not in_signal.integer else 4] = 1
            elif state[4]:  # S4
                next_state[0 if not in_signal.integer else 5] = 1
            elif state[5]:  # S5
                next_state[8 if not in_signal.integer else 6] = 1
            elif state[6]:  # S6
                next_state[9 if not in_signal.integer else 7] = 1
            elif state[7]:  # S7
                next_state[0 if not in_signal.integer else 7] = 1
            elif state[8]:  # S8
                next_state[0 if not in_signal.integer else 1] = 1
            elif state[9]:  # S9
                next_state[0 if not in_signal.integer else 1] = 1

            # Output logic
            out1 = 1 if (state[8] or state[9]) else 0
            out2 = 1 if (state[7] or state[9]) else 0

            # Create output dictionary for this stimulus
            output = {
                "next_state": next_state.binstr,
                "out1": BinaryValue(out1, n_bits=1).binstr,
                "out2": BinaryValue(out2, n_bits=1).binstr,
            }
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
