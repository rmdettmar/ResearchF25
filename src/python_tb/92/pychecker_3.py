import json
from enum import Enum
from typing import Any, Dict, List, Union


class State(Enum):
    A = 0  # Idle state
    B = 1  # Grant to device 1
    C = 2  # Grant to device 2
    D = 3  # Grant to device 3


class GoldenDUT:
    def __init__(self):
        """Initialize internal state registers"""
        self.current_state = State.A
        self.g = 0  # 3-bit output

    def load(self, stimulus_dict: Dict[str, Any]):
        """Process inputs and update state"""
        stimulus_outputs = []

        for stimulus in stimulus_dict["input variable"]:
            # Extract inputs
            resetn = int(stimulus["resetn"], 2)
            r = int(stimulus["r"], 2)  # 3-bit input
            r1 = (r >> 0) & 1
            r2 = (r >> 1) & 1
            r3 = (r >> 2) & 1

            # Handle synchronous reset
            if not resetn:
                self.current_state = State.A
            else:
                # State transitions
                if self.current_state == State.A:
                    if r1:
                        self.current_state = State.B
                    elif r2:
                        self.current_state = State.C
                    elif r3:
                        self.current_state = State.D
                elif self.current_state == State.B:
                    if not r1:
                        self.current_state = State.A
                elif self.current_state == State.C:
                    if not r2:
                        self.current_state = State.A
                elif self.current_state == State.D:
                    if not r3:
                        self.current_state = State.A

            # Generate outputs
            g1 = 1 if self.current_state == State.B else 0
            g2 = 1 if self.current_state == State.C else 0
            g3 = 1 if self.current_state == State.D else 0
            self.g = (g3 << 2) | (g2 << 1) | g1

            # Format output as 3-bit binary string
            g_str = format(self.g, "03b")
            stimulus_outputs.append({"g": g_str})

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
