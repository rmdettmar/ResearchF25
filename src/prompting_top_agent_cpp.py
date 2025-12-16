import argparse
import json
import os
import glob
from datetime import datetime

from . import python_call as py
from .classify_circuit_type import CircuitTypeClassifier
from .gen_tb import TB_Generator
from .gen_tb_scenario import TB_Generator_Scenario
from .gen_tb_seq import TB_Generator_SEQ
from .mage.gen_config import Config
from .mage.log_utils import get_logger, set_log_dir, switch_log_to_file
from .cpp_checker import CppChecker_SEQ


logger = get_logger(__name__)


args_dict = {
    # "model": "deepseek-reasoner",
    # "model": "gpt-4o-2024-08-06",
    # "model": "gpt-4o-mini-2024-07-18",
    # "model": "gemini-2.0-flash",
    # "model": "claude-3-5-sonnet-v2@20241022",
    # "model_fixer": "models/gemini-2.0-flash",
    # "model_fixer": "claude-3-5-sonnet-20241022",
    # "model_fixer": "gpt-4o-2024-08-06",
    # "provider": "anthropic",
    # "provider": "openai",
    # "provider_fixer": "anthropic",
    # "provider_fixer": "openai",
    "temperature": 0,
    "top_p": 1,
    "temperature_sample": 0.3,
    "top_p_sample": 0.95,
    # "model": "claude-3-7-sonnet@20250219",
    # "model": "claude-3-5-sonnet-v2@20241022",
    # "provider": "vertexanthropic",
    # "provider_fixer": "vertexanthropic",
    "model": "gpt-4o-2024-08-06",
    "provider": "openai",
    "provider_fixer": "openai",
     #"task_numbers": [33,36],
    # "task_numbers":  [ 150, 151, 152, 153, 154],
    "task_numbers": [ 4 ],
    # "filter_instance": "Prob051|Prob052|Prob053|Prob054|Prob055|Prob101|Prob102|Prob103|Prob104|Prob105",
    # "filter_instance": "Prob092",
    # "filter_instance": "",
    "folder_path": "./verilog-eval/dataset_spec-to-rtl",
    # "folder_path": "../verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl",
    "run_identifier": "gen_tb",
    "key_cfg_path": "./key.cfg",
    "use_golden_ref": True,
    "max_trials": 5,
}

def get_prob_spec(file_path, task_number):
    # give the file path and task_number, return the problem specification and the header in verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl

    # i don't have their file formats/am using my own, so the readout mechanism needed to change
    # each json is a unique file so there's no need to line-by-line. find original code in testbench_parse.py
    with open(glob.glob(file_path)[0], "r") as f:
        print(f"file_path: {file_path}", f"task_number: {task_number}")
        print(f"file name: {os.path.basename(f.name)}")
        data = json.load(f)
        if data["task_number"] == task_number:
            print(f"header: {data["header"]}")
            print(f"description: {data["description"]}")
            return data["description"], data["header"]
    return None, None


def main():
    args = argparse.Namespace(**args_dict)
    Config(args.key_cfg_path)
    switch_log_to_file()
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"output_tb_{args.run_identifier}_{timestamp}"
    log_dir = f"log_tb_{args.run_identifier}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    print("cwd: ", os.getcwd())

    for task_number in args.task_numbers:

        task_id = task_number
        output_dir_per_task = f"{output_dir}/{task_id}"
        log_dir_per_task = f"{log_dir}/{task_id}"
        os.makedirs(output_dir_per_task, exist_ok=True)
        os.makedirs(log_dir_per_task, exist_ok=True)
        set_log_dir(log_dir_per_task)

        input_spec, header = get_prob_spec((f"{args.folder_path}/Prob{task_number:03}_*.json"), task_number)

        output_results = []
        tb_scenarios_path = os.path.join(output_dir_per_task, f"TB_scenarios.txt")
        stimulus_python_path = os.path.join(output_dir_per_task, f"stimulus.py")
        print("tb_generator_scenario")
        tb_generator_scenario = TB_Generator_Scenario(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            tb_scenarios_path=tb_scenarios_path,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        print("writes stimulus.json")
        tb_generator = TB_Generator(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            stimulus_python_path=stimulus_python_path,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        tb_generator_seq = TB_Generator_SEQ(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            stimulus_python_path=stimulus_python_path,
            temperature=args.temperature,
            top_p=args.top_p,
        )

        cpp_checker = CppChecker_SEQ(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            temperature=args.temperature_sample,
            top_p=args.top_p_sample,
        )
        cpp_checker_seq = CppChecker_SEQ(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            temperature=args.temperature_sample,
            top_p=args.top_p_sample,
        )
        circuit_type_classifier = CircuitTypeClassifier(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        circuit_type_output_json_obj = circuit_type_classifier.run(input_spec)
        circuit_type = circuit_type_output_json_obj["classification"]

        for i in range(args.max_trials):
            cpp_path = os.path.join(output_dir_per_task, f"cppchecker_{i}.cpp")
            print(f"cpp_path: {cpp_path}")
            if circuit_type == "SEQ":
                cpp_checker_seq.run(input_spec, header, cpp_path, circuit_type)
            else:
                cpp_checker.run(input_spec, header, cpp_path, circuit_type)

            # s
            # subproc_call(f"cd {output_dir_per_task}", timeout=120)
            # subproc_call(f"cd {output_dir_per_task}", timeout=120)
            # subproc_call(f"cd {output_dir_per_task}", timeout=120)

if __name__ == "__main__":
    main()
