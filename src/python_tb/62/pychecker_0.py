import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to S0 (one-hot encoding)
        self.current_state = 0b0000000001  # S0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input to BinaryValue
            in_signal = BinaryValue(stimulus["in"])
            state_signal = BinaryValue(stimulus["state"])

            # Calculate next state based on current state and input
            next_state = 0
            current_state = int(state_signal.binstr, 2)

            if in_signal.integer == 0:
                # All 0 transitions go to S0 except S5->S8 and S6->S9
                if current_state & (1 << 5):  # S5
                    next_state = 1 << 8  # Go to S8
                elif current_state & (1 << 6):  # S6
                    next_state = 1 << 9  # Go to S9
                else:
                    next_state = 1  # Go to S0
            else:  # input is 1
                if current_state & 0b0000000001:  # S0
                    next_state = 1 << 1  # Go to S1
                elif current_state & 0b0000000010:  # S1
                    next_state = 1 << 2  # Go to S2
                elif current_state & 0b0000000100:  # S2
                    next_state = 1 << 3  # Go to S3
                elif current_state & 0b0000001000:  # S3
                    next_state = 1 << 4  # Go to S4
                elif current_state & 0b0000010000:  # S4
                    next_state = 1 << 5  # Go to S5
                elif current_state & 0b0000100000:  # S5
                    next_state = 1 << 6  # Go to S6
                elif current_state & 0b0001000000:  # S6
                    next_state = 1 << 7  # Go to S7
                elif current_state & 0b0010000000:  # S7
                    next_state = 1 << 7  # Stay in S7
                elif current_state & 0b0100000000:  # S8
                    next_state = 1 << 1  # Go to S1
                elif current_state & 0b1000000000:  # S9
                    next_state = 1 << 1  # Go to S1

            # Calculate outputs
            out1 = 1 if (current_state & ((1 << 8) | (1 << 9))) else 0
            out2 = 1 if (current_state & ((1 << 7) | (1 << 9))) else 0

            # Format outputs as binary strings
            next_state_bin = format(next_state, "010b")
            out1_bin = format(out1, "01b")
            out2_bin = format(out2, "01b")

            # Add to output list
            stimulus_outputs.append(
                {"next_state": next_state_bin, "out1": out1_bin, "out2": out2_bin}
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
