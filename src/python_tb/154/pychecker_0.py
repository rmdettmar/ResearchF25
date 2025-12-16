import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        # Initialize clock to 12:00:00 AM
        self.hh = 0x12  # BCD 12
        self.mm = 0x00  # BCD 00
        self.ss = 0x00  # BCD 00
        self.pm = 0  # AM

    def increment_bcd(self, value):
        # Increment BCD value
        ones = value & 0x0F
        tens = (value >> 4) & 0x0F

        ones += 1
        if ones > 9:
            ones = 0
            tens += 1
        if tens > 5:
            tens = 0
        return (tens << 4) | ones

    def load(self, stimulus_dict: Dict[str, any]):
        output_list = []

        for stimulus in stimulus_dict["input variable"]:
            # Convert input strings to integers
            reset = int(stimulus["reset"], 2)
            ena = int(stimulus["ena"], 2)

            if reset:
                # Reset to 12:00:00 AM
                self.hh = 0x12
                self.mm = 0x00
                self.ss = 0x00
                self.pm = 0
            elif ena:
                # Increment seconds
                self.ss = self.increment_bcd(self.ss)
                if self.ss == 0x00:
                    # Increment minutes
                    self.mm = self.increment_bcd(self.mm)
                    if self.mm == 0x00:
                        # Increment hours
                        ones = self.hh & 0x0F
                        tens = (self.hh >> 4) & 0x0F

                        ones += 1
                        if ones > 9:
                            ones = 0
                            tens += 1
                        if tens == 1 and ones == 3:
                            # Roll over from 12 to 1
                            tens = 0
                            ones = 1
                            # Toggle AM/PM
                            if self.hh == 0x11:
                                self.pm = not self.pm

                        self.hh = (tens << 4) | ones

            # Convert outputs to binary strings
            out_hh = BinaryValue(value=self.hh, n_bits=8)
            out_mm = BinaryValue(value=self.mm, n_bits=8)
            out_ss = BinaryValue(value=self.ss, n_bits=8)
            out_pm = BinaryValue(value=self.pm, n_bits=1)

            output_list.append(
                {
                    "hh": out_hh.binstr,
                    "mm": out_mm.binstr,
                    "ss": out_ss.binstr,
                    "pm": out_pm.binstr,
                }
            )

        return {"scenario": stimulus_dict["scenario"], "output variable": output_list}


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
