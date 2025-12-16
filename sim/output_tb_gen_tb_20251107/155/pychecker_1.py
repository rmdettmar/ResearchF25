
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        '''
        Initialize all internal state registers to zero.
        '''
        self.state = 'LEFT'  # Initial state is walking left
        self.fall_count = 0
        self.splattered = False

    def load(self, clk, stimulus_dict: dict):
        '''
        Process one clock cycle of the FSM based on the RTL specification.
        '''
        areset = int(stimulus_dict['areset'])
        bump_left = int(stimulus_dict['bump_left'])
        bump_right = int(stimulus_dict['bump_right'])
        ground = int(stimulus_dict['ground'])
        dig = int(stimulus_dict['dig'])

        # Handle asynchronous reset
        if areset == 1:
            self.state = 'LEFT'
            self.fall_count = 0
            self.splattered = False

        if self.splattered:
            return {'walk_left': '0', 'walk_right': '0', 'aaah': '0', 'digging': '0'}

        # On rising edge of clock
        if clk == 1:
            if ground == 0:
                self.fall_count += 1
                if self.fall_count > 20:
                    self.splattered = True
            else:
                self.fall_count = 0

            if self.fall_count > 0:
                # Falling
                outputs = {'walk_left': '0', 'walk_right': '0', 'aaah': '1', 'digging': '0'}
            elif dig == 1 and ground == 1:
                # Digging
                outputs = {'walk_left': '0', 'walk_right': '0', 'aaah': '0', 'digging': '1'}
            else:
                # Walking
                if self.state == 'LEFT':
                    if bump_left == 1:
                        self.state = 'RIGHT'
                    outputs = {'walk_left': '1', 'walk_right': '0', 'aaah': '0', 'digging': '0'}
                elif self.state == 'RIGHT':
                    if bump_right == 1:
                        self.state = 'LEFT'
                    outputs = {'walk_left': '0', 'walk_right': '1', 'aaah': '0', 'digging': '0'}

        else:
            outputs = {'walk_left': '0', 'walk_right': '0', 'aaah': '0', 'digging': '0'}

        return outputs
def check_output(stimulus_list_scenario):

    
    tb_outputs = []


    for stimulus_list in stimulus_list_scenario["input variable"]:
        dut = GoldenDUT()


        clock_cycles = stimulus_list['clock cycles']
        clk = 1
        input_vars_list = {k: v for k, v in stimulus_list.items() if k != "clock cycles"}
        output_vars_list = {'clock cycles':clock_cycles}
        for k,v in input_vars_list.items():
            if len(v) < clock_cycles:
                v.extend([v[-1]] * (clock_cycles - len(v)))
                
        

        for i in range(clock_cycles):
            input_vars = {k:v[i] for k,v in input_vars_list.items()}

            output_vars = dut.load(clk,input_vars)
            for k,v in output_vars.items():
                if k not in output_vars_list:
                    output_vars_list[k] = []
                output_vars_list[k].append(v)
            


        tb_outputs.append(output_vars_list)

    return tb_outputs

if __name__ == "__main__":
    stimulus_file_name = "stimulus.json"
    with open(stimulus_file_name, "r") as f:
        stimulus_data = json.load(f)


    if isinstance(stimulus_data, dict):
        stimulus_list_scenarios = stimulus_data.get("input variable", [])
    else:
        stimulus_list_scenarios = stimulus_data

    outputs=[]
    for stimulus_list_scenario in stimulus_list_scenarios:
        outputs.append( check_output(stimulus_list_scenario))
    with open(stimulus_file_name, "w") as f:
        json.dump(stimulus_list_scenarios, f, indent=4)

    print(json.dumps(outputs, indent=2))





