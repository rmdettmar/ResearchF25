import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize state to OFF (False)
        """
        self.current_state = False  # False=OFF, True=ON

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state according to state machine rules
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            reset_bv = BinaryValue(stimulus["reset"])
            j_bv = BinaryValue(stimulus["j"])
            k_bv = BinaryValue(stimulus["k"])

            # Convert to boolean values
            reset = bool(reset_bv.integer)
            j = bool(j_bv.integer)
            k = bool(k_bv.integer)

            # Update state based on inputs
            if reset:
                self.current_state = False  # Reset to OFF state
            else:
                if not self.current_state:  # OFF state
                    if j:
                        self.current_state = True  # Transition to ON
                else:  # ON state
                    if k:
                        self.current_state = False  # Transition to OFF

            # Output is 1 if in ON state, 0 if in OFF state
            out_value = "1" if self.current_state else "0"
            stimulus_outputs.append({"out": out_value})

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
