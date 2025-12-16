import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # Initialize state registers
        self.state = "A"  # Initial state
        self.count = 0  # Counter for w=1
        self.z = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"])
            s = int(stimulus["s"])
            w = int(stimulus["w"])

            # Handle synchronous reset
            if reset:
                self.state = "A"
                self.count = 0
                self.z = 0
            else:
                # State machine transitions
                if self.state == "A":
                    if s == 1:
                        self.state = "B"
                        self.count = 1 if w == 1 else 0
                elif self.state == "B":
                    self.state = "C"
                    if w == 1:
                        self.count += 1
                elif self.state == "C":
                    self.state = "D"
                    if w == 1:
                        self.count += 1
                elif self.state == "D":
                    self.state = "E"
                    if w == 1:
                        self.count += 1
                elif self.state == "E":
                    self.state = "B"
                    self.z = 1 if self.count == 2 else 0
                    self.count = 1 if w == 1 else 0

            stimulus_outputs.append({"z": str(self.z)})

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
