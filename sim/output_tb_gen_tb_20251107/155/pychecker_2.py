
import json
from typing import Dict, List, Union


class GoldenDUT:
    def __init__(self):
        '''
        Initialize all internal state registers to zero.
        '''
        self.state = 'WALK_LEFT'  # Initial state after reset
        self.fall_time = 0  # Counter for fall time
        # Outputs
        self.walk_left = 0
        self.walk_right = 0
        self.aaah = 0
        self.digging = 0
        
    def load(self, clk, stimulus_dict):
        '''
        Update state on rising edge of clock based on inputs.
        '''
        # Parse inputs
        areset = int(stimulus_dict['areset'], 2)
        bump_left = int(stimulus_dict['bump_left'], 2)
        bump_right = int(stimulus_dict['bump_right'], 2)
        ground = int(stimulus_dict['ground'], 2)
        dig = int(stimulus_dict['dig'], 2)

        if areset == 1:
            self.state = 'WALK_LEFT'
            self.fall_time = 0

        elif clk == 1:
            if self.state == 'FALLING':
                self.fall_time += 1
                if ground == 1:
                    if self.fall_time > 20:
                        self.state = 'SPLAT'
                    else:
                        self.fall_time = 0
                        if self.prev_state == 'WALK_LEFT':
                            self.state = 'WALK_LEFT'
                        else:
                            self.state = 'WALK_RIGHT'
            elif self.state == 'DIGGING':
                if ground == 0:
                    self.state = 'FALLING'
                    self.fall_time = 1
                # Digging continues until ground disappears
            elif self.state in ['WALK_LEFT', 'WALK_RIGHT']:
                if ground == 0:
                    self.state = 'FALLING'
                    self.fall_time = 1
                elif dig == 1:
                    self.state = 'DIGGING'
                else:
                    if self.state == 'WALK_LEFT' and bump_left == 1:
                        self.state = 'WALK_RIGHT'
                    elif self.state == 'WALK_RIGHT' and bump_right == 1:
                        self.state = 'WALK_LEFT'

        # Update outputs based on current state
        self.walk_left = 1 if self.state == 'WALK_LEFT' else 0
        self.walk_right = 1 if self.state == 'WALK_RIGHT' else 0
        self.aaah = 1 if self.state == 'FALLING' else 0
        self.digging = 1 if self.state == 'DIGGING' else 0

        return {
            'walk_left': str(self.walk_left),
            'walk_right': str(self.walk_right),
            'aaah': str(self.aaah),
            'digging': str(self.digging)
        }
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





