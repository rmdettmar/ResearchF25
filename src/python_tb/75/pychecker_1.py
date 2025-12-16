import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize state variables
        self.state = 0  # Track sequence position
        self.start_shifting = 0  # Output signal

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input signals to proper format
            reset = BinaryValue(stimulus["reset"]).integer
            data = BinaryValue(stimulus["data"]).integer

            # Process reset
            if reset:
                self.state = 0
                self.start_shifting = 0
            else:
                # If already found sequence, maintain start_shifting
                if self.start_shifting:
                    pass
                else:
                    # FSM state transitions
                    if self.state == 0:
                        if data == 1:
                            self.state = 1
                    elif self.state == 1:
                        if data == 1:
                            self.state = 2
                        else:
                            self.state = 0
                    elif self.state == 2:
                        if data == 0:
                            self.state = 3
                        else:
                            self.state = 2
                    elif self.state == 3:
                        if data == 1:
                            self.state = 0
                            self.start_shifting = 1  # Sequence found!
                        else:
                            self.state = 0

            # Append output to results
            stimulus_outputs.append(
                {"start_shifting": format(self.start_shifting, "b")}
            )

        output_dict = {
            "scenario": stimulus_dict["scenario"],
            "output variable": stimulus_outputs,
        }

        return output_dict


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
