import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        """
        Initialize state registers
        """
        self.p_reg = 0  # Output p register
        self.q_reg = 0  # Output q register
        self.prev_clock = 0  # Previous clock value
        self.prev_p = 0  # Previous p value

    def load(self, stimulus_dict: Dict[str, any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            clock = int(stimulus["clock"])
            a = int(stimulus["a"])

            # Rising edge detection
            if clock == 1 and self.prev_clock == 0:
                self.p_reg = a

            # Falling edge detection
            if clock == 0 and self.prev_clock == 1:
                if self.p_reg == 0 and self.prev_p == 1:
                    self.q_reg = 1
                if self.p_reg == 0 and self.prev_p == 0:
                    self.q_reg = 0

            # Update previous values
            self.prev_clock = clock
            self.prev_p = self.p_reg

            # Add current outputs to stimulus_outputs
            stimulus_outputs.append({"p": str(self.p_reg), "q": str(self.q_reg)})

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
