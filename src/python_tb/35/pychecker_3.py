import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state tracking
        self.state = BinaryValue("0000000001", n_bits=10)  # Start in state S

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            d = int(stimulus.get("d", "0"))
            done_counting = int(stimulus.get("done_counting", "0"))
            ack = int(stimulus.get("ack", "0"))
            state = int(stimulus.get("state", self.state.binstr), 2)

            # Compute next states
            S_next = (
                ((state & 0b0000000001) and not d)
                or ((state & 0b0000000010) and not d)
                or ((state & 0b0000001000) and not d)
                or ((state & 0b1000000000) and ack)
            )

            S1_next = (state & 0b0000000001) and d

            B3_next = state & 0b01000000

            Count_next = (state & 0b10000000) or (
                (state & 0b100000000) and not done_counting
            )

            Wait_next = ((state & 0b100000000) and done_counting) or (
                (state & 0b1000000000) and not ack
            )

            # Compute outputs
            shift_ena = bool(state & 0b0111110000)
            counting = bool(state & 0b0100000000)
            done = bool(state & 0b1000000000)

            # Create output dictionary
            output = {
                "B3_next": str(int(B3_next)),
                "S_next": str(int(S_next)),
                "S1_next": str(int(S1_next)),
                "Count_next": str(int(Count_next)),
                "Wait_next": str(int(Wait_next)),
                "done": str(int(done)),
                "counting": str(int(counting)),
                "shift_ena": str(int(shift_ena)),
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
