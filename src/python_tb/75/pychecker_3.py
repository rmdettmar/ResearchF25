import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize state variables:
        - current_state: tracks FSM state (0-3)
        - start_shifting_reg: output register
        """
        self.current_state = 0
        self.start_shifting_reg = 0

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and update state machine
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to integers
            reset = int(stimulus["reset"])
            data = int(stimulus["data"])

            # Handle reset
            if reset:
                self.current_state = 0
                self.start_shifting_reg = 0
            else:
                # State machine logic
                if (
                    not self.start_shifting_reg
                ):  # Only process if sequence not yet found
                    if self.current_state == 0:
                        if data == 1:
                            self.current_state = 1
                    elif self.current_state == 1:
                        if data == 1:
                            self.current_state = 2
                        else:
                            self.current_state = 0
                    elif self.current_state == 2:
                        if data == 0:
                            self.current_state = 3
                        else:
                            self.current_state = 1
                    elif self.current_state == 3:
                        if data == 1:
                            self.start_shifting_reg = 1  # Sequence found!
                            self.current_state = 0
                        else:
                            self.current_state = 0

            # Append current output to results
            stimulus_outputs.append({"start_shifting": str(self.start_shifting_reg)})

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
