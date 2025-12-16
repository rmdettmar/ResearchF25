import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize the 4-digit BCD counter state"""
        self.q = 0  # 16-bit counter value
        self.ena = [0] * 3  # enable signals for digits [3:1]

    def _is_digit_nine(self, digit_val):
        """Check if a BCD digit is 9"""
        return digit_val == 9

    def _increment_bcd(self, val):
        """Increment a BCD digit, handling wrap-around"""
        return 0 if val == 9 else val + 1

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and update counter state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)

            if reset:
                self.q = 0
                self.ena = [0] * 3
            else:
                # Extract current digits
                digit0 = self.q & 0xF
                digit1 = (self.q >> 4) & 0xF
                digit2 = (self.q >> 8) & 0xF
                digit3 = (self.q >> 12) & 0xF

                # Calculate enables
                self.ena[0] = 1 if self._is_digit_nine(digit0) else 0  # ena[1]
                self.ena[1] = (
                    1 if self._is_digit_nine(digit1) and self.ena[0] else 0
                )  # ena[2]
                self.ena[2] = (
                    1 if self._is_digit_nine(digit2) and self.ena[1] else 0
                )  # ena[3]

                # Increment digits
                digit0 = self._increment_bcd(digit0)
                if self.ena[0]:
                    digit1 = self._increment_bcd(digit1)
                if self.ena[1]:
                    digit2 = self._increment_bcd(digit2)
                if self.ena[2]:
                    digit3 = self._increment_bcd(digit3)

                # Combine digits
                self.q = (digit3 << 12) | (digit2 << 8) | (digit1 << 4) | digit0

            # Prepare output
            q_bv = BinaryValue(value=self.q, n_bits=16)
            ena_bv = BinaryValue(
                value=sum(v << i for i, v in enumerate(self.ena)), n_bits=3
            )

            output_dict = {"q": q_bv.binstr, "ena": ena_bv.binstr}
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
