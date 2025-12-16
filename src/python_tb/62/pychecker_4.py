import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to S0 (one-hot encoding)
        self.current_state = BinaryValue("0000000001", n_bits=10)

    def load(self, stimulus_dict: Dict[str, Any]) -> Dict[str, Any]:
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get input signal
            input_signal = BinaryValue(stimulus["in"])
            state_signal = BinaryValue(stimulus["state"], n_bits=10)

            # Calculate next state based on current state and input
            next_state = BinaryValue("0000000000", n_bits=10)

            # State transition logic
            if state_signal[0] == 1:  # S0
                next_state[0 if input_signal == 0 else 1] = 1
            elif state_signal[1] == 1:  # S1
                next_state[0 if input_signal == 0 else 2] = 1
            elif state_signal[2] == 1:  # S2
                next_state[0 if input_signal == 0 else 3] = 1
            elif state_signal[3] == 1:  # S3
                next_state[0 if input_signal == 0 else 4] = 1
            elif state_signal[4] == 1:  # S4
                next_state[0 if input_signal == 0 else 5] = 1
            elif state_signal[5] == 1:  # S5
                next_state[8 if input_signal == 0 else 6] = 1
            elif state_signal[6] == 1:  # S6
                next_state[9 if input_signal == 0 else 7] = 1
            elif state_signal[7] == 1:  # S7
                next_state[0 if input_signal == 0 else 7] = 1
            elif state_signal[8] == 1:  # S8
                next_state[0 if input_signal == 0 else 1] = 1
            elif state_signal[9] == 1:  # S9
                next_state[0 if input_signal == 0 else 1] = 1

            # Output logic
            out1 = 1 if (state_signal[8] == 1 or state_signal[9] == 1) else 0
            out2 = 1 if (state_signal[7] == 1 or state_signal[9] == 1) else 0

            # Prepare output dictionary
            output = {
                "next_state": next_state.binstr,
                "out1": BinaryValue(out1).binstr,
                "out2": BinaryValue(out2).binstr,
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
