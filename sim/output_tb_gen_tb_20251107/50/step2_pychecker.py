
import json
from typing import Dict, List, Union

class GoldenDUT:

    def __init__(self):
        pass

    def load(self, stimulus_dict: Dict[str, any]):
        a = int(stimulus_dict['a'], 2)
        b = int(stimulus_dict['b'], 2)
        c = int(stimulus_dict['c'], 2)
        # Corrected to perform OR operation to match the RTL logic
        out = (a | b | c)
        out_str = f'{out:b}'
        return {'out': out_str}
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


