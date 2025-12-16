import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize clock to 12:00:00 AM
        self.pm = False
        self.hh = 0x12  # BCD 12
        self.mm = 0x00  # BCD 00
        self.ss = 0x00  # BCD 00

    def increment_bcd(self, value):
        # Increment BCD value with proper rollover
        ones = value & 0x0F
        tens = (value >> 4) & 0x0F

        ones += 1
        if ones > 9:
            ones = 0
            tens += 1
            if tens > 5:
                tens = 0

        return (tens << 4) | ones

    def increment_hours_bcd(self, value):
        # Special case for hours (1-12)
        ones = value & 0x0F
        tens = (value >> 4) & 0x0F

        ones += 1
        if ones > 9:
            ones = 0
            tens += 1
        if tens == 1 and ones > 2:
            tens = 0
            ones = 1

        return (tens << 4) | ones

    def load(self, stimulus_dict: Dict[str, any]):
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
                self.ss = self.increment_bcd(self.ss)
                if self.ss == 0x00:
                    # Increment minutes
                    self.mm = self.increment_bcd(self.mm)
                    if self.mm == 0x00:
                        # Increment hours
                        self.hh = self.increment_hours_bcd(self.hh)
                        if self.hh == 0x12:
                            # Toggle AM/PM
                            self.pm = not self.pm

            # Convert outputs to BinaryValue format
            pm_bv = BinaryValue(value=1 if self.pm else 0, n_bits=1)
            hh_bv = BinaryValue(value=self.hh, n_bits=8)
            mm_bv = BinaryValue(value=self.mm, n_bits=8)
            ss_bv = BinaryValue(value=self.ss, n_bits=8)

            stimulus_outputs.append(
                {
                    "pm": pm_bv.binstr,
                    "hh": hh_bv.binstr,
                    "mm": mm_bv.binstr,
                    "ss": ss_bv.binstr,
                }
            )

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
