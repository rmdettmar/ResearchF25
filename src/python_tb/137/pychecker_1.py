import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state machine to reset state B
        """
        self.STATE_A = 0
        self.STATE_B = 1
        self.current_state = self.STATE_B  # Reset state is B

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to state machine logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals from binary strings to integers
            reset_bv = BinaryValue(stimulus["reset"])
            in_bv = BinaryValue(stimulus["in"])
            reset = reset_bv.integer
            in_signal = in_bv.integer

            # Handle reset
            if reset:
                self.current_state = self.STATE_B
            else:
                # State transition logic
                if self.current_state == self.STATE_B:
                    if in_signal == 0:
                        self.current_state = self.STATE_A
                else:  # current_state == STATE_A
                    if in_signal == 0:
                        self.current_state = self.STATE_B

            # Output logic - Moore machine output only depends on current state
            out = 1 if self.current_state == self.STATE_B else 0

            # Convert output to binary string format
            out_bv = BinaryValue(value=out, n_bits=1)
            stimulus_outputs.append({"out": out_bv.binstr})

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
