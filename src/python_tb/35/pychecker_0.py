import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.state = BinaryValue("0000000001", n_bits=10)  # Initial state S

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            d = int(stimulus.get("d", "0"))
            done_counting = int(stimulus.get("done_counting", "0"))
            ack = int(stimulus.get("ack", "0"))
            state = int(stimulus.get("state", self.state.integer))

            # Convert state to one-hot format
            current_state = BinaryValue(value=state, n_bits=10)

            # Calculate next states
            S = current_state[0]
            S1 = current_state[1]
            S11 = current_state[2]
            S110 = current_state[3]
            B0 = current_state[4]
            B1 = current_state[5]
            B2 = current_state[6]
            B3 = current_state[7]
            Count = current_state[8]
            Wait = current_state[9]

            # Calculate next state logic
            B3_next = B2
            S_next = (S & ~d) | (S1 & ~d) | (S110 & ~d) | (Wait & ack)
            S1_next = S & d
            Count_next = B3 | (Count & ~done_counting)
            Wait_next = (Count & done_counting) | (Wait & ~ack)

            # Calculate outputs
            shift_ena = 1 if (B0 or B1 or B2 or B3) else 0
            counting = 1 if Count else 0
            done = 1 if Wait else 0

            # Create output dictionary for this stimulus
            output = {
                "B3_next": str(int(B3_next)),
                "S_next": str(int(S_next)),
                "S1_next": str(int(S1_next)),
                "Count_next": str(int(Count_next)),
                "Wait_next": str(int(Wait_next)),
                "done": str(done),
                "counting": str(counting),
                "shift_ena": str(shift_ena),
            }
            outputs.append(output)

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
