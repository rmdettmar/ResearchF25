import argparse
import json
import os
import re
from datetime import datetime

from classify_circuit_type import CircuitTypeClassifier
from .mage.gen_config import Config
from .mage.log_utils import get_logger, set_log_dir, switch_log_to_file

logger = get_logger(__name__)

args_dict = {
    "temperature": 0,
    "top_p": 1,
    "model": "claude-3-5-sonnet-v2@20241022",
    "provider": "vertexanthropic",
    "provider_fixer": "vertexanthropic",
    "folder_path": "../verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl",
    "run_identifier": "ambiguous_casestudy",
    "key_cfg_path": "../key.cfg",
    "use_golden_ref": True,
    "task_numbers": range(31, 155),
    "output_dir": "../ambiguous_llm_as_judge",
}


def get_prob_spec(file_path, task_number):
    with open(file_path, "r") as f:
        print(f"file_path: {file_path}", f"task_number: {task_number}")
        for line in f:
            data = json.loads(line)
            if data["task_number"] == task_number:
                return data["description"], data["header"]
    return None, None


def main():
    args = argparse.Namespace(**args_dict)
    Config(args.key_cfg_path)
    switch_log_to_file()

    classifier = CircuitTypeClassifier(
        model=args.model,
        max_token=8192,
        provider=args.provider,
        cfg_path=args.key_cfg_path,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"output_circuit_type_{args.run_identifier}_{timestamp}"
    log_dir = f"log_circuit_type_{args.run_identifier}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

    summary_file_path = os.path.join(output_dir, "summary_circuit_type_casestudy.txt")
    summary = []

    for task_number in args.task_numbers:
        task_id = task_number
        output_dir_per_task = f"{output_dir}/{task_id}"
        log_dir_per_task = f"{log_dir}/{task_id}"
        os.makedirs(output_dir_per_task, exist_ok=True)
        os.makedirs(log_dir_per_task, exist_ok=True)
        set_log_dir(log_dir_per_task)

        input_spec, header = get_prob_spec(args.folder_path, task_number)
        if input_spec is None:
            continue

        output_json_obj = classifier.run(input_spec)

        classification = output_json_obj["classification"]
        reasoning = output_json_obj["reasoning"]
        output_file_path = os.path.join(output_dir_per_task, f"check_circuit_type.json")
        with open(output_file_path, "w") as output_file:
            json.dump(output_json_obj, output_file, indent=4)
        summary.append(
            f"Task: {task_id}, Circuit Type: {classification}, Reasoning: {reasoning}\n"
        )
        print(f"Task: {task_id}, Circuit Type: {classification}")

    summary.sort()
    with open(summary_file_path, "a") as summary_file:
        summary_file.writelines(summary)


if __name__ == "__main__":
    main()
