import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # States
        self.STATE_A = 0
        self.STATE_B = 1

        # Initialize state variables
        self.current_state = self.STATE_A
        self.cycle_count = 0
        self.w_count = 0
        self.z_out = 0

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert inputs to integers
            reset = int(stimulus["reset"], 2)
            s = int(stimulus["s"], 2)
            w = int(stimulus["w"], 2)

            # Handle reset
            if reset:
                self.current_state = self.STATE_A
                self.cycle_count = 0
                self.w_count = 0
                self.z_out = 0
            else:
                # State machine logic
                if self.current_state == self.STATE_A:
                    if s == 1:
                        self.current_state = self.STATE_B
                        self.cycle_count = 0
                        self.w_count = 0

                elif self.current_state == self.STATE_B:
                    # Count w=1 occurrences
                    if w == 1:
                        self.w_count += 1

                    self.cycle_count += 1

                    # After 3 cycles
                    if self.cycle_count == 3:
                        # Set output for next cycle
                        self.z_out = 1 if self.w_count == 2 else 0
                        # Reset counters for next 3-cycle check
                        self.cycle_count = 0
                        self.w_count = 0

            # Append current output to results
            stimulus_outputs.append({"z": format(self.z_out, "b")})

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
