import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize 4 BCD digits (16 bits total)
        self.q_reg = 0  # All digits start at 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)

            if reset:
                # Synchronous reset - clear all digits
                self.q_reg = 0
                ena_out = 0
            else:
                # Extract current digits
                digit0 = self.q_reg & 0xF
                digit1 = (self.q_reg >> 4) & 0xF
                digit2 = (self.q_reg >> 8) & 0xF
                digit3 = (self.q_reg >> 12) & 0xF

                # Calculate next digit values
                digit0 = (digit0 + 1) % 10
                ena1 = 1 if digit0 == 0 else 0

                if ena1:
                    digit1 = (digit1 + 1) % 10
                ena2 = 1 if (ena1 and digit1 == 0) else 0

                if ena2:
                    digit2 = (digit2 + 1) % 10
                ena3 = 1 if (ena2 and digit2 == 0) else 0

                if ena3:
                    digit3 = (digit3 + 1) % 10

                # Combine enable signals
                ena_out = (ena3 << 2) | (ena2 << 1) | ena1

                # Update state register
                self.q_reg = (digit3 << 12) | (digit2 << 8) | (digit1 << 4) | digit0

            # Format outputs
            output_dict = {
                "q": format(self.q_reg, "016b"),
                "ena": format(ena_out, "03b"),
            }
            stimulus_outputs.append(output_dict)

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
