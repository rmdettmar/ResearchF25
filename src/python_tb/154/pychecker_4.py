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

    def load(self, stimulus_dict: Dict[str, Any]):
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
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
                ss_low = self.ss & 0x0F
                ss_high = (self.ss >> 4) & 0x0F

                ss_low += 1
                if ss_low > 9:
                    ss_low = 0
                    ss_high += 1
                    if ss_high > 5:
                        ss_high = 0
                        # Increment minutes
                        mm_low = self.mm & 0x0F
                        mm_high = (self.mm >> 4) & 0x0F

                        mm_low += 1
                        if mm_low > 9:
                            mm_low = 0
                            mm_high += 1
                            if mm_high > 5:
                                mm_high = 0
                                # Increment hours
                                hh_low = self.hh & 0x0F
                                hh_high = (self.hh >> 4) & 0x0F

                                if self.hh == 0x12:  # 12 -> 1
                                    self.hh = 0x01
                                    if (
                                        mm_high == 0
                                        and mm_low == 0
                                        and ss_high == 0
                                        and ss_low == 0
                                    ):
                                        self.pm = not self.pm
                                else:
                                    hh_low += 1
                                    if hh_low > 9:
                                        hh_low = 0
                                        hh_high += 1
                                    if hh_high == 1 and hh_low == 3:  # 13 -> 1
                                        self.hh = 0x01
                                    else:
                                        self.hh = (hh_high << 4) | hh_low

                self.mm = (mm_high << 4) | mm_low
                self.ss = (ss_high << 4) | ss_low

            # Convert outputs to BinaryValue
            hh_bv = BinaryValue(value=self.hh, n_bits=8)
            mm_bv = BinaryValue(value=self.mm, n_bits=8)
            ss_bv = BinaryValue(value=self.ss, n_bits=8)
            pm_bv = BinaryValue(value=self.pm, n_bits=1)

            output = {
                "hh": hh_bv.binstr,
                "mm": mm_bv.binstr,
                "ss": ss_bv.binstr,
                "pm": pm_bv.binstr,
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
