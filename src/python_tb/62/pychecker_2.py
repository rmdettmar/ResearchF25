import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize to state S0 (one-hot encoding)
        self.current_state = 1  # state[0] = 1, others = 0

    def load(self, stimulus_dict: Dict[str, any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input to BinaryValue
            in_signal = BinaryValue(stimulus["in"])
            state_signal = BinaryValue(stimulus["state"])

            # Calculate next state based on current state and input
            current_state_idx = state_signal.integer.bit_length() - 1
            next_state = 0

            # State transition logic
            if in_signal.integer == 0:
                # All states go to S0 on input 0 except S5 and S6
                if state_signal[5] == 1:
                    next_state = 1 << 8  # Go to S8
                elif state_signal[6] == 1:
                    next_state = 1 << 9  # Go to S9
                else:
                    next_state = 1  # Go to S0
            else:  # input is 1
                if state_signal[0] == 1:  # S0
                    next_state = 1 << 1  # Go to S1
                elif state_signal[1] == 1:  # S1
                    next_state = 1 << 2  # Go to S2
                elif state_signal[2] == 1:  # S2
                    next_state = 1 << 3  # Go to S3
                elif state_signal[3] == 1:  # S3
                    next_state = 1 << 4  # Go to S4
                elif state_signal[4] == 1:  # S4
                    next_state = 1 << 5  # Go to S5
                elif state_signal[5] == 1:  # S5
                    next_state = 1 << 6  # Go to S6
                elif state_signal[6] == 1:  # S6
                    next_state = 1 << 7  # Go to S7
                elif state_signal[7] == 1:  # S7
                    next_state = 1 << 7  # Stay in S7
                elif state_signal[8] == 1 or state_signal[9] == 1:  # S8 or S9
                    next_state = 1 << 1  # Go to S1

            # Calculate outputs
            out1 = 1 if (state_signal[8] == 1 or state_signal[9] == 1) else 0
            out2 = 1 if (state_signal[7] == 1 or state_signal[9] == 1) else 0

            # Format outputs as binary strings
            next_state_bin = BinaryValue(value=next_state, n_bits=10, bigEndian=False)
            out1_bin = BinaryValue(value=out1, n_bits=1, bigEndian=False)
            out2_bin = BinaryValue(value=out2, n_bits=1, bigEndian=False)

            output_list.append(
                {
                    "next_state": next_state_bin.binstr,
                    "out1": out1_bin.binstr,
                    "out2": out2_bin.binstr,
                }
            )

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
