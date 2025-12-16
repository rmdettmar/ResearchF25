import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 16-bit counter register
        self.q_reg = 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Get reset signal
            reset = int(BinaryValue(stimulus["reset"]).value)

            if reset:
                # Synchronous reset - clear counter
                self.q_reg = 0
            else:
                # Process each digit
                # Ones digit (always enabled)
                digit0 = self.q_reg & 0xF
                digit0 = (digit0 + 1) % 10

                # Enable signals for higher digits
                ena1 = 1 if (self.q_reg & 0xF) == 9 else 0
                ena2 = 1 if (ena1 and ((self.q_reg >> 4) & 0xF) == 9) else 0
                ena3 = 1 if (ena2 and ((self.q_reg >> 8) & 0xF) == 9) else 0

                # Update higher digits
                digit1 = (self.q_reg >> 4) & 0xF
                digit1 = (digit1 + 1) % 10 if ena1 else digit1

                digit2 = (self.q_reg >> 8) & 0xF
                digit2 = (digit2 + 1) % 10 if ena2 else digit2

                digit3 = (self.q_reg >> 12) & 0xF
                digit3 = (digit3 + 1) % 10 if ena3 else digit3

                # Combine all digits
                self.q_reg = (digit3 << 12) | (digit2 << 8) | (digit1 << 4) | digit0

            # Create output dictionary for this stimulus
            output = {
                "q": format(self.q_reg, "016b"),
                "ena": format((ena3 << 2) | (ena2 << 1) | ena1, "03b"),
            }
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
