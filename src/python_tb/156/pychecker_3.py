import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """
        Initialize internal state registers
        q[15:0] - 16-bit counter (4 BCD digits)
        """
        self.q_reg = 0  # 16-bit counter initialized to 0

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(BinaryValue(stimulus["reset"]).value)

            if reset:
                # Synchronous reset - clear all digits
                self.q_reg = 0
                ena_out = 0
            else:
                # Extract current digits
                ones = self.q_reg & 0xF
                tens = (self.q_reg >> 4) & 0xF
                hundreds = (self.q_reg >> 8) & 0xF
                thousands = (self.q_reg >> 12) & 0xF

                # Calculate next digit values and enable signals
                ena1 = 1 if ones == 9 else 0
                ena2 = 1 if ones == 9 and tens == 9 else 0
                ena3 = 1 if ones == 9 and tens == 9 and hundreds == 9 else 0

                # Update ones digit
                ones = (ones + 1) if ones < 9 else 0

                # Update tens digit
                if ena1:
                    tens = (tens + 1) if tens < 9 else 0

                # Update hundreds digit
                if ena2:
                    hundreds = (hundreds + 1) if hundreds < 9 else 0

                # Update thousands digit
                if ena3:
                    thousands = (thousands + 1) if thousands < 9 else 0

                # Combine all digits
                self.q_reg = (thousands << 12) | (hundreds << 8) | (tens << 4) | ones
                ena_out = (ena3 << 2) | (ena2 << 1) | ena1

            # Format outputs
            output = {"q": format(self.q_reg, "016b"), "ena": format(ena_out, "03b")}
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
