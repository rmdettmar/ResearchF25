import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state to S (first bit set in one-hot encoding)
        self.current_state = 0b0000000001

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            d = int(stimulus["d"])
            done_counting = int(stimulus["done_counting"])
            ack = int(stimulus["ack"])
            state = int(stimulus["state"])

            # Calculate next state bits
            S = state & 0b0000000001
            S1 = state & 0b0000000010
            S11 = state & 0b0000000100
            S110 = state & 0b0000001000
            B0 = state & 0b0000010000
            B1 = state & 0b0000100000
            B2 = state & 0b0001000000
            B3 = state & 0b0010000000
            Count = state & 0b0100000000
            Wait = state & 0b1000000000

            # Calculate next state logic
            B3_next = B2
            S_next = (S & ~d) | (S1 & ~d) | (S110 & ~d) | (Wait & ack)
            S1_next = S & d
            Count_next = (B3) | (Count & ~done_counting)
            Wait_next = (Count & done_counting) | (Wait & ~ack)

            # Calculate outputs
            shift_ena = 1 if (B0 or B1 or B2 or B3) else 0
            counting = 1 if Count else 0
            done = 1 if Wait else 0

            # Create output dictionary for this stimulus
            output = {
                "B3_next": str(B3_next),
                "S_next": str(S_next),
                "S1_next": str(S1_next),
                "Count_next": str(Count_next),
                "Wait_next": str(Wait_next),
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
