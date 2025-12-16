import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        """
        self.counter = 0  # Counter to track cycles
        self.shift_ena_reg = 0  # Output register

    def load(self, stimulus_dict: Dict[str, any]):
        """
        Process inputs and generate outputs according to FSM logic
        """
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert binary string inputs to integers
            reset = int(stimulus["reset"], 2)

            # FSM logic
            if reset:
                # Reset condition - start counter and enable shift
                self.counter = 0
                self.shift_ena_reg = 1
            elif self.shift_ena_reg:
                # If shift is enabled, increment counter
                if self.counter >= 3:
                    # After 4 cycles (0,1,2,3), disable shift
                    self.shift_ena_reg = 0
                self.counter = self.counter + 1

            # Format output as binary string
            shift_ena_str = format(self.shift_ena_reg, "b")
            stimulus_outputs.append({"shift_ena": shift_ena_str})

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
