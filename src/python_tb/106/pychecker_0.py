import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.p_reg = 0
        self.q_reg = 0
        self.prev_p = 0
        self.prev_clk = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to BinaryValue objects
            clock = BinaryValue(stimulus["clock"]).integer
            a = BinaryValue(stimulus["a"]).integer

            # Detect positive clock edge
            if clock == 1 and self.prev_clk == 0:
                # Update p register
                self.p_reg = a

                # Update q register
                if a == 0:
                    self.q_reg = 0

            # Detect p falling edge (outside clock edge)
            if self.prev_p == 1 and self.p_reg == 0:
                self.q_reg = 1

            # Store previous values
            self.prev_clk = clock
            self.prev_p = self.p_reg

            # Create output dictionary
            output = {"p": format(self.p_reg, "b"), "q": format(self.q_reg, "b")}
            stimulus_outputs.append(output)

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
