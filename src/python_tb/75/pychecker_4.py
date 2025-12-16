
import json
from enum import Enum
from typing import Any, Dict, List, Union

from cocotb.binary import BinaryValue


class GoldenDUT:
    class State(Enum):
        IDLE = 0    # Looking for first '1'
        GOT1 = 1    # Got first '1'
        GOT11 = 2   # Got '11'
        GOT110 = 3  # Got '110'
        FOUND = 4   # Found '1101'

    def __init__(self):
        '''Initialize internal state registers'''
        self.current_state = self.State.IDLE
        self.start_shifting = 0

    def load(self, stimulus_dict: Dict[str, any]):
        '''Process inputs and generate outputs'''
        outputs = []

        for stimulus in stimulus_dict['input variable']:
            # Convert input strings to BinaryValue objects
            reset = BinaryValue(stimulus['reset']).integer
            data = BinaryValue(stimulus['data']).integer

            # Handle reset
            if reset:
                self.current_state = self.State.IDLE
                self.start_shifting = 0
            else:
                # State machine transitions
                if self.current_state == self.State.IDLE:
                    if data == 1:
                        self.current_state = self.State.GOT1
                elif self.current_state == self.State.GOT1:
                    if data == 1:
                        self.current_state = self.State.GOT11
                    else:
                        self.current_state = self.State.IDLE
                elif self.current_state == self.State.GOT11:
                    if data == 0:
                        self.current_state = self.State.GOT110
                    else:
                        self.current_state = self.State.GOT11
                elif self.current_state == self.State.GOT110:
                    if data == 1:
                        self.current_state = self.State.FOUND
                        self.start_shifting = 1
                    else:
                        self.current_state = self.State.IDLE
                # Once in FOUND state, stay there until reset

            # Append current output to outputs list
            outputs.append({'start_shifting': f"{self.start_shifting:01b"})

        return {
            'scenario': stimulus_dict['scenario'],
            'output variable': outputs
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
