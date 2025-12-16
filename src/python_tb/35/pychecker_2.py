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
            # Convert inputs to BinaryValue
            d = int(stimulus["d"])
            done_counting = int(stimulus["done_counting"])
            ack = int(stimulus["ack"])
            state = BinaryValue(stimulus["state"], n_bits=10)

            # Calculate next states
            B3_next = state[5] == "1"  # B2 -> B3
            S_next = (
                (state[0] == "1" and d == 0)
                or (state[1] == "1" and d == 0)
                or (state[3] == "1" and d == 0)
                or (state[9] == "1" and ack == 1)
            )
            S1_next = state[0] == "1" and d == 1
            Count_next = (state[7] == "1") or (  # B3 -> Count
                state[8] == "1" and not done_counting
            )
            Wait_next = (state[8] == "1" and done_counting) or (
                state[9] == "1" and not ack
            )

            # Calculate outputs
            shift_ena = (
                state[4] == "1" or state[5] == "1" or state[6] == "1" or state[7] == "1"
            )
            counting = state[8] == "1"
            done = state[9] == "1"

            # Create output dictionary for this stimulus
            output = {
                "B3_next": "1" if B3_next else "0",
                "S_next": "1" if S_next else "0",
                "S1_next": "1" if S1_next else "0",
                "Count_next": "1" if Count_next else "0",
                "Wait_next": "1" if Wait_next else "0",
                "done": "1" if done else "0",
                "counting": "1" if counting else "0",
                "shift_ena": "1" if shift_ena else "0",
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
