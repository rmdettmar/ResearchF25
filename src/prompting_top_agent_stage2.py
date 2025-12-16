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
from .gen_tb_scenario_cmb import TB_Generator_Scenario_CMB
from .check_consistency_cmb import ConsistencyChecker_cmb
from .check_consistency import ConsistencyChecker
from .gen_config import Config
from .pychecker import PyChecker
from .pychecker_seq import PyChecker_SEQ
from .tb_extract import TBExtractor
from .testbench_parse import process_testbench, create_testbench_json, create_testbench_json_cmb, get_prob_spec
from .judge_for_RTL import JudgeForRTL

from .log_utils import get_logger, set_log_dir, switch_log_to_file
from .utils.to_png import text_to_png

logger = get_logger(__name__)


args_dict = {
    # "model": "deepseek-reasoner",
    # "model": "gpt-4o-2024-08-06",
    # "model": "gpt-4o-mini-2024-07-18",
    # "model": "gemini-2.0-flash",
   # "model": "claude-3-5-sonnet-v2@20241022",
    # "model_fixer": "claude-3-5-sonnet-20241022",
    # "model": "claude-3-5-sonnet-20241022",
    # "model_fixer": "gpt-4o-2024-08-06",
    #  "provider": "anthropic",
    # "provider": "openai",
    # "provider_fixer": "anthropic",
    # "provider_fixer": "openai",
    # "model": "gpt-4o-2024-08-06",
    # "model_fixer": "gpt-4o-2024-08-06",
    "model": "gpt-4o",
    "model_fixer": "gpt-4o",
    "provider": "openai",
    "provider_fixer": "openai",
    
    "temperature": 1,
    "top_p": 1,
    "temperature_sample": 0.3,
    "top_p_sample": 0.95,
    "max_token": 8192,
    # "model": "claude-3-7-sonnet@20250219",
   # "model": "claude-3-5-sonnet-v2@20241022",
    #"provider": "vertexanthropic",
    # "provider_fixer": "anthropic",
    "task_numbers": [ 16 ],
    # "task_numbers": range(6, 8),
    # "filter_instance": "Prob051|Prob052|Prob053|Prob054|Prob055|Prob101|Prob102|Prob103|Prob104|Prob105",
    # "filter_instance": "Prob092",
    # "filter_instance": "",
    "folder_path": "./verilog-eval/dataset_spec-to-rtl",
    # "folder_path": "../verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl",
    "run_identifier": "gen_tb",
    "key_cfg_path": "./key.cfg",
    "use_golden_ref": True,
    'sampling_size': 2,
    'stimuli_sampling_size': 3,
    "max_trials": 5,
    "stage": 1,
    "day": "20251108",
    "circuit_type": "SEQ",
    "spec_filetype": "png", # png or txt
}




def main():
    args = argparse.Namespace(**args_dict)
    day=args.day
    Config(args.key_cfg_path)
    switch_log_to_file()
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"output_tb_{args.run_identifier}_{day}"
    log_dir = f"log_tb_{args.run_identifier}_{day} "
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    circuit_type = args.circuit_type
    
    python_correctness_list = []
    for task_number in args.task_numbers:
        output_results = []

        task_id = task_number
        output_dir_per_task = f"{output_dir}/{task_id}"
        log_dir_per_task = f"{log_dir}/{task_id}"
        os.makedirs(output_dir_per_task, exist_ok=True)
        os.makedirs(log_dir_per_task, exist_ok=True)
        set_log_dir(log_dir_per_task)

        # STAGES 1 & 2
        # Initialize all LLM generator interfaces
        if args.stage <= 2:
            #input_spec, header = get_prob_spec((f"{args.folder_path}/Prob{task_number:03}_*.json"), task_number)
            input_spec, header = get_prob_spec((f"{args.folder_path}/all_tasks.jsonl"), task_number)


            tb_scenarios_path = os.path.join(output_dir_per_task, f"TB_scenarios.txt")
            stimulus_python_path = os.path.join(output_dir_per_task, f"stimulus")
            judge_for_rtl = JudgeForRTL(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            tb_generator_scenario = TB_Generator_Scenario(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                tb_scenarios_path=tb_scenarios_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            tb_generator_scenario_cmb = TB_Generator_Scenario_CMB(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                tb_scenarios_path=tb_scenarios_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            tb_generator = TB_Generator(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                stimulus_python_path=stimulus_python_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            consistency_checker = ConsistencyChecker(args.model, args.max_token, args.provider, args.key_cfg_path, args.top_p, args.temperature, output_dir, task_number)
            consistency_checker_cmb = ConsistencyChecker_cmb(args.model, args.max_token, args.provider, args.key_cfg_path, args.top_p, args.temperature, output_dir, task_number)
            tb_generator_seq = TB_Generator_SEQ(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                stimulus_python_path=stimulus_python_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )
            tb_extractor = TBExtractor(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                temperature=args.temperature,
                top_p=args.top_p,
            )

            py_checker = PyChecker(
                model=args.model,
                max_token=8192,
                provider=args.provider,
                cfg_path=args.key_cfg_path,
                temperature=args.temperature_sample,
                top_p=args.top_p_sample,
            )
            py_checker_seq = PyChecker_SEQ(
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
            if args.circuit_type == "CMB":
                circuit_type = "CMB"
            else:
                circuit_type_output_json_obj = circuit_type_classifier.run(input_spec)
                circuit_type = circuit_type_output_json_obj["classification"]
        
        # STAGE 1 ONLY
        if args.stage <= 1:
            if circuit_type == "CMB":
                tb_generator_scenario_cmb.run(input_spec, header, circuit_type)
            else:
                tb_generator_scenario.run(input_spec, header, circuit_type)
                
            tb_scenario_description = open(tb_scenarios_path, "r").read()
            print(f"tb_scenario_description: {tb_scenario_description}")

            # this one in particular seems to be extremely unsuccessful (at least with gpt5)
            # if args.spec_filetype == "png":
            #     text_to_png(os.path.join(output_dir_per_task, f"TB_scenarios.txt"), os.path.join(output_dir_per_task, f"TB_scenarios.png"))
            #     tb_scenario_description = os.path.join(output_dir_per_task, f"TB_scenarios.png")

            print("starting stimulus.py generation")
            if circuit_type == "SEQ":
                stimulus_result = tb_generator_seq.run(
                    input_spec,
                    header,
                    tb_scenario_description,
                    circuit_type,
                    stimuli_sampling_size=args.stimuli_sampling_size,
                    scenarios_filetype=args.spec_filetype,
                )
            else:
                stimulus_result = tb_generator.run(
                    input_spec,
                    header,
                    tb_scenario_description,
                    circuit_type,
                    stimuli_sampling_size=args.stimuli_sampling_size,
                    scenarios_filetype=args.spec_filetype,
                )
        
        # ALL STAGES
        # subproc_call(f"cd {output_dir_per_task}", timeout=120)
        stimulus_result = py.python_call_and_save(
            f"{output_dir_per_task}/stimulus.py", silent=True
        )
        print(f"stimulus_result: {stimulus_result}")

        return

        # STAGES 1 & 2
        if args.stage <= 2:
            
            refined_input_spec = tb_extractor.run(input_spec)
            with open(f"{output_dir_per_task}/spec.txt", "w") as f:
                f.write(refined_input_spec["revised_spec"])
            input_spec = refined_input_spec["revised_spec"]
            if args.spec_filetype == "png": # if a png, actually get png path
                text_to_png(f"{output_dir_per_task}/spec.txt", f"{output_dir_per_task}/spec.png")
                input_spec = f"{output_dir_per_task}/spec.png"

            # for i in range(args.max_trials):
            for i in range(2):
                python_path = os.path.join(output_dir_per_task, f"pychecker_{i}.py")
                print(f"python_path: {python_path}")
                if circuit_type == "SEQ":
                        gen_python_code=py_checker_seq.run(input_spec, header, python_path, circuit_type, args.spec_filetype)
                else:
                        gen_python_code=py_checker.run(input_spec, header, python_path, circuit_type, args.spec_filetype)

                # subproc_call(f"cd {output_dir_per_task}", timeout=120)
                # subproc_call(f"cd {output_dir_per_task}", timeout=120)


        # ALL STAGES
        for trial in range(args.max_trials):       
            for i in range(args.sampling_size):
                output_results.append(
                    py.python_call_and_save(
                        f"{output_dir_per_task}/pychecker_{i}.py", silent=True, timeout=120
                    )
                )

                try:
                    output_str = "\n".join(str(result) for result in output_results)
                    output_file_path = os.path.join(output_dir_per_task, f"our_output.txt")
                    with open(output_file_path, "w") as output_file:
                        output_file.write(output_str)
                except Exception as e:
                    logger.error(f"Error writing output file: {e}")
                    logger.error(f"Output results: {output_results}")

        if circuit_type == "CMB":
            create_testbench_json_cmb(
                f"{output_dir_per_task}/stimulus.json",
                f"{output_dir_per_task}/our_output.txt",
                f"{output_dir_per_task}/testbench.json",
            )
            testbench_dict = process_testbench(f"{output_dir_per_task}/testbench.json")
            print(testbench_dict)
            with open(f"{output_dir_per_task}/testbench.json", 'w') as f:
                json.dump(testbench_dict, f, indent=2, ensure_ascii=False)
        else:
            create_testbench_json(
                f"{output_dir_per_task}/stimulus.json",
                f"{output_dir_per_task}/our_output.txt",
                f"{output_dir_per_task}/testbench.json",
            )

        with open(glob.glob(f"{args.folder_path}/Prob{task_number:03}_*_ref.sv")[0]) as f:
            rtl_code = f.read()
        refined_python_code, python_correctness = judge_for_rtl.run(input_spec, rtl_code, gen_python_code, circuit_type, args.spec_filetype)
        python_correctness_list.append(python_correctness)
        with open(f"{output_dir_per_task}/step2_pychecker.py", "w") as f:
            f.write(refined_python_code)

        refined_output_results = []
        refined_output_results.append(
                    py.python_call_and_save(
                        f"{output_dir_per_task}/step2_pychecker.py", silent=True, timeout=120
                    )
                )

        refined_output_str = "\n".join(str(result) for result in refined_output_results)
        refined_output_file_path = os.path.join(output_dir_per_task, f"step2_our_output.txt")
        with open(refined_output_file_path, "w") as refined_output_file:
            refined_output_file.write(refined_output_str)
            refined_output_file.flush()  # Ensure data is written to disk
            os.fsync(refined_output_file.fileno())  # Force synchronization to disk
            
        # Ensure file exists and is not empty
        if not os.path.exists(refined_output_file_path) or os.path.getsize(refined_output_file_path) == 0:
            logger.error(f"Output file {refined_output_file_path} does not exist or is empty")
            return
            
        if circuit_type == "CMB":
            create_testbench_json_cmb(
                f"{output_dir_per_task}/stimulus.json",
                f"{output_dir_per_task}/step2_our_output.txt",
                f"{output_dir_per_task}/step2_testbench.json",
            )
            testbench_dict = process_testbench(f"{output_dir_per_task}/step2_testbench.json")
            with open(f"{output_dir_per_task}/step2_testbench.json", 'w') as f:
                json.dump(testbench_dict, f, indent=2, ensure_ascii=False)
        else:
            create_testbench_json(
                f"{output_dir_per_task}/stimulus.json",
                f"{output_dir_per_task}/step2_our_output.txt",
                f"{output_dir_per_task}/step2_testbench.json",
            )

    python_correctness_list_file_path = os.path.join(f"python_correctness_list.txt")
    with open(python_correctness_list_file_path, "w") as f:
        f.write(str(python_correctness_list))

        

    # summary.sort()
    # with open(summary_file_path, "a") as summary_file:
    #    summary_file.writelines(summary)


if __name__ == "__main__":
    main()
