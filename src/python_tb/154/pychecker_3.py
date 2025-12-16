import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize internal state registers
        self.pm = False
        self.hh = 0x12  # Start at 12 (BCD)
        self.mm = 0x00
        self.ss = 0x00

    def _increment_bcd(self, value, max_tens, max_ones):
        ones = value & 0x0F
        tens = (value >> 4) & 0x0F

        ones += 1
        if ones > 9:
            ones = 0
            tens += 1
            if tens > max_tens:
                tens = 0
                return True, 0  # Rollover occurred
        if (tens * 10 + ones) > max_ones:
            tens = 0
            ones = 0
            return True, 0  # Rollover occurred
        return False, (tens << 4) | ones

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)
            ena = int(stimulus["ena"], 2)

            if reset:
                # Reset to 12:00:00 AM
                self.pm = False
                self.hh = 0x12
                self.mm = 0x00
                self.ss = 0x00
            elif ena:
                # Increment seconds
                rollover, self.ss = self._increment_bcd(self.ss, 5, 59)
                if rollover:
                    # Increment minutes
                    rollover, self.mm = self._increment_bcd(self.mm, 5, 59)
                    if rollover:
                        # Increment hours
                        if self.hh == 0x11:
                            self.hh = 0x12
                            self.pm = not self.pm  # Toggle AM/PM
                        elif self.hh == 0x12:
                            self.hh = 0x01
                        else:
                            _, self.hh = self._increment_bcd(self.hh, 1, 12)

            # Create output dictionary for this stimulus
            output = {
                "pm": "1" if self.pm else "0",
                "hh": BinaryValue(value=self.hh, n_bits=8).binstr,
                "mm": BinaryValue(value=self.mm, n_bits=8).binstr,
                "ss": BinaryValue(value=self.ss, n_bits=8).binstr,
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
