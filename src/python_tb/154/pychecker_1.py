import json
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    def __init__(self):
        """Initialize clock state to 12:00:00 AM"""
        self.pm = 0
        self.hh = 0x12  # BCD 12
        self.mm = 0x00  # BCD 00
        self.ss = 0x00  # BCD 00

    def _bcd_increment(self, value, max_tens, max_ones):
        """Helper to increment BCD value with rollover"""
        ones = value & 0x0F
        tens = (value >> 4) & 0x0F

        ones += 1
        if ones > max_ones:
            ones = 0
            tens += 1
            if tens > max_tens:
                tens = 0
                return 0, True
        return (tens << 4) | ones, False

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            reset = int(stimulus["reset"], 2)
            ena = int(stimulus["ena"], 2)

            if reset:
                # Reset to 12:00:00 AM
                self.pm = 0
                self.hh = 0x12
                self.mm = 0x00
                self.ss = 0x00
            elif ena:
                # Increment seconds
                self.ss, rollover = self._bcd_increment(self.ss, 5, 9)
                if rollover:
                    # Increment minutes
                    self.mm, rollover = self._bcd_increment(self.mm, 5, 9)
                    if rollover:
                        # Increment hours
                        if self.hh == 0x12:
                            self.hh = 0x01
                        else:
                            self.hh, rollover = self._bcd_increment(self.hh, 1, 9)
                            if self.hh == 0x12:
                                # Toggle AM/PM when going from 11:59:59 to 12:00:00
                                self.pm = not self.pm

            # Convert outputs to binary strings
            pm_bv = BinaryValue(value=self.pm, n_bits=1)
            hh_bv = BinaryValue(value=self.hh, n_bits=8)
            mm_bv = BinaryValue(value=self.mm, n_bits=8)
            ss_bv = BinaryValue(value=self.ss, n_bits=8)

            output = {
                "pm": pm_bv.binstr,
                "hh": hh_bv.binstr,
                "mm": mm_bv.binstr,
                "ss": ss_bv.binstr,
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
