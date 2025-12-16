import json
import glob
import os
import ast

def get_prob_spec(file_path, task_number):
    with open(glob.glob(file_path)[0], "r") as f:
        print(f"file_path: {file_path}", f"task_number: {task_number}")
        print(f"file name: {os.path.basename(f.name)}")
        datai = f.readlines()
        for line in datai:
            data = json.loads(line)
            # print(data)

            if data["task_number"] == task_number:
                print(f"header: {data["header"]}")
                print(f"description: {data["description"]}")
                return data["description"], data["header"]
    return None, None

def get_prob_spec_single(file_path, task_number):
    # give the file path and task_number, return the problem specification and the header in verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl

    # i don't have their file formats/am using my own, so the readout mechanism needed to change
    # each json is a unique file so there's no need to line-by-line. original method is listed below.
    with open(glob.glob(file_path)[0], "r") as f:
        print(f"file_path: {file_path}", f"task_number: {task_number}")
        print(f"file name: {os.path.basename(f.name)}")
        data = json.load(f)
        if data["task_number"] == task_number:
            print(f"header: {data["header"]}")
            print(f"description: {data["description"]}")
            return data["description"], data["header"]
        
        # datai = f.read()
        # for line in datai:
        #     data = json.loads(datai)
        #     print(data)

        #     if data["task_number"] == task_number:
        #         print(f"header: {data["header"]}")
        #         print(f"description: {data["description"]}")
        #         return data["description"], data["header"]
    return None, None

# def get_prob_spec(file_path, task_number):
#     # give the file path and task_number, return the problem specification and the header in verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl

#     with open(glob.glob(file_path)[0], "r") as f:
#         print(f"file_path: {file_path}", f"task_number: {task_number}")
#         print(f"file name: {os.path.basename(f.name)}")
#         datai = f.read()
#         for line in f:
#             data = json.loads(line)

#             if data["task_number"] == task_number:
#                 # print(f"data: {data}")
#                 return data["description"], data["header"]
#     return None, None


def process_testbench(json_file):
    # Read JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Convert to required dictionary format
    testbench = []
    for scenario in data:
        for i in range(len(scenario['input variable'])):
            print(f"{scenario['output variable'][i]}: {scenario['input variable'][i]}")
            scenario_name = scenario['scenario']+str(i)
            testbench.append({
                'scenario': scenario_name,
                'input variable':[ scenario['input variable'][i]],
                'output variable': [scenario['output variable'][i]]
            })
    
    return testbench

def create_testbench_json(stimulus_file, output_file, output_json_file):
   
    # Read stimulus.json to get input data
    with open(stimulus_file, "r") as f:
        stimulus_data = json.load(f)

    # Read our_output.txt to get output data
    with open(output_file, "r") as f:
        output_lines = f.readlines()

    # Parse output data
    all_outputs = []
    for line in output_lines:

        parsed = ast.literal_eval(line)
        if parsed[0] and "out" in parsed[1]:
            # Parse JSON string
            try:
                output_str = parsed[1]["out"].strip()
                # If output is a list-formatted string, remove leading and trailing brackets
                if output_str.startswith('[') and output_str.endswith(']'):
                    output_str = output_str[1:-1]
                # Try to parse as JSON
                output_data = json.loads(f"[{output_str}]")
                all_outputs.extend(output_data)  # Expand output data list
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"Problematic data: {output_str}")
                continue

    # If no valid output, exit
    if not all_outputs:
        print("No valid output data found")
        return

    # Use the last complete output as standard result
    standard_output = all_outputs  # Use the last output
    # Merge input and output
    combined_data = []

    # Iterate through each test scenario
    for i, stimulus_scenario in enumerate(stimulus_data):
        scenario_name = stimulus_scenario["scenario"]
        # Create merged scenario data
        for j in stimulus_scenario["input variable"]:
            for key,item in j.items():
                if key!="clock cycles":
                    if len(item) < j["clock cycles"]:
                        print(f"item: {item} is less than clock cycles: {j['clock cycles']}")
                        item.extend([item[-1]]*(j["clock cycles"]-len(item)))
        combined_scenario = {
            "scenario": scenario_name,
            "input variable": stimulus_scenario["input variable"],
        }
        combined_scenario["output variable"] = []
        
        for x, j in enumerate(combined_scenario["input variable"]):
            temp_output = {}
            temp_output["clock cycles"] = j["clock cycles"]
            temp_output.update(standard_output[i][x])
            combined_scenario["output variable"].append(temp_output)
        combined_data.append(combined_scenario)

    # Write merged data to JSON file
    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully merged stimulus and output data to {output_json_file}")


def create_testbench_json_cmb(stimulus_file, output_file, output_json_file):
    """
    Merge stimulus.json and our_output.txt into a complete testbench.json file
    
    Parameters:
    stimulus_file -- stimulus.json file path
    output_file -- our_output.txt file path
    output_json_file -- output testbench.json file path
    """
    # Read stimulus.json to get input data
    with open(stimulus_file, 'r') as f:
        stimulus_data = json.load(f)
    
    # Read our_output.txt to get output data
    with open(output_file, 'r') as f:
        output_lines = f.readlines()
    all_outputs = []
    for line in output_lines:

        parsed = ast.literal_eval(line)
        if parsed[0] and "out" in parsed[1]:
            # Parse JSON string
            try:
                output_str = parsed[1]["out"].strip()
                # If output is a list-formatted string, remove leading and trailing brackets
                if output_str.startswith('[') and output_str.endswith(']'):
                    output_str = output_str[1:-1]
                # Try to parse as JSON
                output_data = json.loads(f"[{output_str}]")
                all_outputs.extend(output_data)  # Expand output data list
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"Problematic data: {output_str}")
                continue
    

    # If no valid output, exit
    if not all_outputs:
        print("No valid output data found")
        return
    
    # Check if there are inconsistencies in all output groups
    # Only use the first output group as standard result
    standard_output = all_outputs
    print(f"standard_output: {standard_output}")
    
    # Merge input and output
    combined_data = []
    
    # Iterate through each test scenario
    for i, stimulus_scenario in enumerate(stimulus_data):
        scenario_name = stimulus_scenario['scenario']
        
        # Find corresponding scenario in output data
        output_scenario = standard_output[i]
        
        if output_scenario:
            # Create merged scenario data
            combined_scenario = {
                "scenario": scenario_name,
                "input variable": stimulus_scenario['input variable'],
                "output variable": output_scenario
            }
            combined_data.append(combined_scenario)
        else:
            print(f"Warning: Scenario '{scenario_name}' not found in output data")
            # Add scenario without output
            combined_scenario = {
                "scenario": scenario_name,
                "input variable": stimulus_scenario['input variable'],
                "output variable": []
            }
            combined_data.append(combined_scenario)
    
    # Write merged data to JSON file
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully merged stimulus and output data to {output_json_file}")

