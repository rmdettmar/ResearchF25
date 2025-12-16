import argparse
import json
import os
import glob
from datetime import datetime

from .gen_mutants import MutantGenerator
from src.gen_config import Config
from src.log_utils import get_logger, set_log_dir, switch_log_to_file

args_dict = {
    "model": "gpt-4o-2024-08-06",
    "model_fixer": "gpt-4o-2024-08-06",
    "provider": "openai",
    "provider_fixer": "openai",
    "temperature": 0,
    "top_p": 1,
    "temperature_sample": 0.3,
    "top_p_sample": 0.95,
    "max_token": 8192,
    "task_numbers": [ 156 ],
    "run_identifier": "gen_tb",
    "key_cfg_path": "./key.cfg",
    "rtl_path": "./verilog-eval/dataset_spec-to-rtl",
    "day": "20251107",
}

def get_verilog(file_path, task_number):
    with open(glob.glob(file_path)[0], "r") as f:
        print(f"file_path: {file_path}", f"task_number: {task_number}")
        print(f"file name: {os.path.basename(f.name)}")
        data = f.read()
        return data
    return None

def main():
    args = argparse.Namespace(**args_dict)
    day=args.day
    Config(args.key_cfg_path)
    switch_log_to_file()
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"mutant_verilog_{day}"
    log_dir = f"log_mutants_{day}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    for task_id in args.task_numbers:
        output_results = []
        output_dir_per_task = f"{output_dir}/{task_id}"
        log_dir_per_task = f"{log_dir}/{task_id}"
        os.makedirs(output_dir_per_task, exist_ok=True)
        os.makedirs(log_dir_per_task, exist_ok=True)
        
        mutator = MutantGenerator(
            model=args.model,
            max_token=8192,
            provider=args.provider,
            cfg_path=args.key_cfg_path,
            temperature=args.temperature,
            top_p=args.top_p,
        )

        module = get_verilog((f"{args.rtl_path}/Prob{task_id:03}_*_ref.sv"), task_id)
        
        mutator.run(mutants_path=output_dir_per_task, golden_module=module)

if __name__ == "__main__":
    main()