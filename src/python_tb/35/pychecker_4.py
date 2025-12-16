import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state indices
        self.S = 0
        self.S1 = 1
        self.S11 = 2
        self.S110 = 3
        self.B0 = 4
        self.B1 = 5
        self.B2 = 6
        self.B3 = 7
        self.Count = 8
        self.Wait = 9

    def load(self, stimulus_dict: Dict[str, any]):
        outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to boolean/integer
            d = BinaryValue(stimulus["d"]).integer
            done_counting = BinaryValue(stimulus["done_counting"]).integer
            ack = BinaryValue(stimulus["ack"]).integer
            state = BinaryValue(stimulus["state"]).integer

            # Determine current state from one-hot encoding
            current_state = 0
            for i in range(10):
                if state & (1 << i):
                    current_state = i
                    break

            # Calculate next states
            B3_next = 1 if current_state == self.B2 else 0
            S_next = (
                1
                if (current_state == self.S and not d)
                or (current_state == self.S1 and not d)
                or (current_state == self.S110 and not d)
                or (current_state == self.Wait and ack)
                else 0
            )
            S1_next = 1 if (current_state == self.S and d) else 0
            Count_next = (
                1
                if (current_state == self.B3)
                or (current_state == self.Count and not done_counting)
                else 0
            )
            Wait_next = (
                1
                if (current_state == self.Count and done_counting)
                or (current_state == self.Wait and not ack)
                else 0
            )

            # Calculate outputs
            shift_ena = (
                1 if current_state in [self.B0, self.B1, self.B2, self.B3] else 0
            )
            counting = 1 if current_state == self.Count else 0
            done = 1 if current_state == self.Wait else 0

            result = {
                "B3_next": str(B3_next),
                "S_next": str(S_next),
                "S1_next": str(S1_next),
                "Count_next": str(Count_next),
                "Wait_next": str(Wait_next),
                "done": str(done),
                "counting": str(counting),
                "shift_ena": str(shift_ena),
            }
            outputs.append(result)

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
