
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        # No state needed for combinational logic
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        # Translate the Karnaugh map into a truth table with Gray code ordering
        _TRUTH_TABLE = {
            '000': '1',  # a=0, b=0, c=0
            '001': 'd',  # a=0, b=0, c=1
            '011': '1',  # a=0, b=1, c=1
            '010': '0',  # a=0, b=1, c=0
            '110': '1',  # a=1, b=1, c=0
            '111': 'd',  # a=1, b=1, c=1
            '101': '0',  # a=1, b=0, c=1
            '100': '0'   # a=1, b=0, c=0
        }

        a, b, c = stimulus_dict['a'], stimulus_dict['b'], stimulus_dict['c']
        key = a + b + c  # Construct the lookup key

        # Evaluate the truth table for the given input
        out = _TRUTH_TABLE.get(key, '0')  # Default to '0' if not found
        if out == 'd':
            out = '0'  # Handle don't-care by assigning to 0

        return {'out': out}

def check_output(stimulus):

    dut = GoldenDUT()


        

    return dut.load(stimulus)

if __name__ == "__main__":

    with open("stimulus.json", "r") as f:
        stimulus_data = json.load(f)

    stimulus_list = []
    for stimulus in stimulus_data:
        stimulus_list.append(stimulus['input variable'])

    tb_outputs = []
    for stimulus in stimulus_list:
        scenario_outputs=[]
        for cycle in stimulus:

            outputs = check_output(cycle)
            scenario_outputs.append(outputs)
        tb_outputs.append(scenario_outputs)


    

    print(json.dumps(tb_outputs, indent=2))


