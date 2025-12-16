import json
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import os
from datetime import datetime

import json
from typing import Dict

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from .mage.gen_config import get_llm
from .mage.log_utils import get_logger
from .mage.prompts import ORDER_PROMPT
from .mage.token_counter import TokenCounter, TokenCounterCached
from .mage.gen_config import Config
from .mage.log_utils import get_logger, set_log_dir, switch_log_to_file
logger = get_logger(__name__)

SYSTEM_PROMPT = """
You are an expert in RTL design and verification.
"""
INIT_EDITION_PROMPT = """

Your task is to review a natural-language RTL specification and input/output signal data (in JSON format) for a combinational circuit.
 "scenario": "scenarioNameNoPunctuation",
  "input variable": \[
    {{
      "input_variable_name1": "binary_value_1", // input_variable_name1: binary value for this input signal
      "input_variable_name2": "binary_value_2",
      "input_variable_name3": "binary_value_3"
    }}\]
  "output variable": \[
    {{
      "output_variable_name1": "binary_value_1", // output_variable_name1: binary value that should appear immediately in response to inputs
      "output_variable_name2": "binary_value_2",
      "output_variable_name3": "binary_value_3"
    }}\]

You must think step by step to determine whether the observed input/output behavior matches the expected logic described in the RTL specification for this combinational circuit.
Firstly, think about the core functionality scenarios that test the main logical operations of the combinational circuit.
Secondly, analyze the relationship between inputs and outputs:
1. Examine each input combination and its corresponding output.
2. Verify that outputs change immediately and only in response to input changes (no timing dependencies).
3. Check that the same input combinations always produce the same outputs (combinational behavior).
4. Verify that outputs do not depend on any previous input states.
5. Check if the logical operations specified in the RTL are correctly implemented.
If there are mismatches, identify them and propose or describe the needed actions to resolve them (or highlight the issues).

The following information is provided to assist your work:
1. RTL specification: A natural-language RTL specification describing the expected combinational logic behavior.
2. imperfect_output: Input/output signal data (in JSON format) might or might not match the specification showing various input combinations and their corresponding outputs.

<RTL specification>
{spec}
</RTL specification>

<module_header>
{module_header}
</module_header>

<imperfect_output>
{testbench}
</imperfect_output>

[Task]:
1. **Interpret the RTL specification** and understand the intended combinational logic. 
To complete this task, follow these steps:

1. Analyze the RTL specification:
   - Identify the key logical operations and expected behavior
   - Determine the expected input/output relationships
   - Note any specific logical constraints or requirements

2. Analyze the I/O data:
   - Parse the JSON data to understand input combinations and their outputs
   - Verify that each input combination has a unique corresponding output
   - Check for any unexpected state-dependent behavior

3. Compare the expected behavior with the observed behavior:
   - Verify that each input combination produces the correct output according to the specification
   - Check that the logical operations are implemented correctly
   - Ensure all specified functionality is demonstrated in the test cases

4. Secondly, analyze the relationship between inputs and outputs: Pay special attention to bit-width and bit-ordering. Examine each input combination and its corresponding output. 
[Very Important]

In RTL descriptions, a signal is typically defined with a range notation like [m:n]:

The first number (m) is the leftmost position in the bit vector
The second number (n) is the rightmost position
String to Bit Position Mapping
Examine each input combination and its corresponding output position:
For descending order [m] where m > n (typical RTL):

If a signal is defined as x[4:0], then the binary value '11100' corresponds to:

x4=1 (leftmost digit in string)
x3=1
x2=1
x1=0
x0=0 (rightmost digit in string)


If a signal is defined as x[3:1], then the binary value '100' corresponds to:

x3=1 (leftmost digit in string)
x2=0
x1=0 (rightmost digit in string)

For codes y[3:1], Y2 is the middle bit.

[Hint]

0. Perform bitwise consistency checks for all 01 sequences: Confirm input/output bit lengths match. Verify no duplicate minterms in truth tables. Cross-check Karnaugh map groupings against standard adjacency rules. When detecting non-standard ordering in inputs, check the order of outputs. 

1. Karnaugh Maps:
example:
// ab
// cd 00 01 11 10
// 00 | 1 | 0 | 1 | 1 |
// 01 | 0 | 1 | 0 | 1 |
// 11 | 1 | 1 | 0 | 0 |
// 10 | 1 | 0 | 0 | 0 |
To interpret the table:
The columns (left to right) represent the values of ab = 00, 01, 11, 10
The rows (top to bottom) represent the values of cd = 00, 01, 11, 10
Each cell contains the function output f(a, b, c, d) for the corresponding combination of a, b, c, and d.
Make sure that the key 'abcd' is constructed with: a and b from the column label (left to right: 00, 01, 11, 10), c and d from the row label (top to bottom: 00, 01, 11, 10), So the top-third cell corresponds to a=1, b=1, c=0, d=0 → '0011'
eg. For a = 1, b = 1, c = 1, d = 0, look at row cd = 10 and column ab = 11; the value is 0, so f(1, 1, 1, 0) = 0.
For a = 1, b = 0, c = 1, d = 0, look at row cd = 10 and column ab = 10; the value is 0, so f(1, 0, 1, 0) = 0. 

3. For finite state machine, the next state is determined by the current state and the input. You need to generate the truth table which includes all the possible combinations of the current state and the input. For example,    
 _TRUTH_TABLE = {{
            '0000': '1',  # S0 + w=0 → S1 → y0 = 1
            '0001': '0',  # S0 + w=1 → S2 → y0 = 0
            '0010': '1',  # S1 + w=0 → S3 → y0 = 1
            '0011': '0',  # S1 + w=1 → S4 → y0 = 0
            '0100': '0',  # S2 + w=0 → S4 → y0 = 0
            '0101': '1',  # S2 + w=1 → S5 → y0 = 1
            '0110': '1',  # S3 + w=0 → S5 → y0 = 1
            '0111': '0',  # S3 + w=1 → S0 → y0 = 0
            
            
        }}


When encountering Karnaugh maps in specifications:
-  Please construct a `_TRUTH_TABLE` dictionary representing the circuit logic, where:
   - Each key is a binary string representing the input combination, ordered using **Gray code** for Karnaugh map alignment.
   Make sure that the key 'abcd' is constructed with: a and b from the column label (left to right: 00, 01, 11, 10), c and d from the row label (top to bottom: 00, 01, 11, 10), So the top-third cell corresponds to a=1, b=1, c=0, d=0 → '0011'.

   - Each value is either 0 or 1, corresponding to the output for that input.
   - Don't-care (`d`) entries should be resolved in a way that simplifies logic (you may assign them to 0).
   - For any unspecified or ambiguous input (e.g., variables named `x` or unused in K-map), default the value to 0.
- Follow these rules strictly:
   - All input variables must be used in the Gray code order to construct the lookup key.
   - If a variable does not appear in the Karnaugh map (e.g., labeled `x` or not mentioned), treat it as `0` during simulation.
   - Only logic lookup is allowed, no procedural conditionals like `if/else` are permitted.

<reasoning>
1. RTL Specification Summary:
   [Briefly summarize the key logical operations and expected behavior]

2. I/O Data Analysis:
   [Describe the observed input/output relationships]

3. Comparison and Mismatches:
   [List and describe any mismatches between the specification and observed behavior]
</reasoning>

3. **Review the testbench** and compare the observed input/output combinations against the expected behavior from the RTL specification.
4. Determine whether the observed behavior **matches** or **does not match** what the specification dictates.
   - If it does not match, **identify** and **describe** the mismatch or possible cause of the discrepancy.
5. Compile the results into the final structure, producing a scenario-by-scenario breakdown:
   - For each scenario (e.g., "Scenario1", "Scenario2", etc.):
     - Provide a short textual explanation of the reasoning (why you believe it matches or not).
     - Indicate "yes" or "no" for `if matches`.
     - If "no", fill in `unmatched action` with a brief explanation of the mismatch or an action you would take to resolve it.

<example>
{example}
</example>
"""
EXTRA_ORDER_PROMPT = """
VERY IMPORTANT: Please only include "reasoning" and "result" in your response.
Do not include any other information in your response, like 'json', 'example', 'Let me analyze','input_spec' or '<output_format>'.
Key instruction: Direct output, no extra comments.
As a reminder, please directly provide the content without adding any extra comments or explanations.
"""

EXAMPLE_OUTPUT_FORMAT = {
    "reasoning": "All reasoning steps, think step by step which scenario is most significant to the functionality of the design",
    "functionality_reasoning": "Reasoning if the functionality of the json file matches the specification",
    "edge_reasoning": "Reasoning if the edge cases of the json file matches the specification",
    "result": [
        {
            "name": "key scenario1",
            "input/output_variable_correlations": "the correlations between input and output variables",
            "explanation": "Here's why it matches or does not match.",
            "if_matches": "yes/no",
            "input_variable": "the input in the testbench.json that in the scenario does not match the specification",
            "unmatched_present_output": "the present output in the testbench.json that does not match the specification",
            'correct_output': "the correct output that should be in the testbench.json",
        },
        {
            "name": "key scenario2",
            "input/output_variable_correlations": "the correlations between input and output variables",
            "explanation": "Here's why it matches or does not match.",
            "if_matches": "yes/no",
            "input_variable": "the input in the testbench.json that in the scenario does not match the specification",
            "unmatched_present_output": "the present output in the testbench.json that does not match the specification",
            'correct_output': "the correct output that should be in the testbench.json",
        },
        
    ],
}

ACTION_OUTPUT_PROMPT = r"""
Output after running given action:
<action_output>
{action_output}
</action_output>
"""

example = """
<spec>
Consider the state machine shown below:

// A (0) --0--> B
// A (0) --1--> A
// B (0) --0--> C
// B (0) --1--> D
// C (0) --0--> E
// C (0) --1--> D
// D (0) --0--> F
// D (0) --1--> A
// E (1) --0--> E
// E (1) --1--> D
// F (1) --0--> C
// F (1) --1--> D

// Assume that you want to Implement the FSM using three flip-flops and state codes y[3:1] = 000, 001, ..., 101 for states A, B, ..., F, respectively. Implement just the next-state logic for y[2] in Verilog. The output Y2 is y[2].
</spec>

<imperfect_output>
  {
    "scenario": "FromStateB_Transitions0",
    "input variable": [
      {
        "y": "001",
        "w": "0"
      }
    ],
    "output variable": [
      {
        "Y2": "0"
      }
    ]
  }
</imperfect_output>
<reasoning>
When y=001 and w=0, the next state should be D(100). The expected output is 1, but the imperfect output is 0.
</reasoning>
<result>
{
    "name": "FromStateB_Transitions0",
    "input/output_variable_correlations": "Y2 is the middle bit of the next state",
    "explanation": "Here's why it matches or does not match.",
    "if_matches": "no",
}
"""


class ConsistencyChecker:
    def __init__(
        self,
        model: str,
        max_token: int,
        provider: str,
        cfg_path: str,
        top_p: float,
        temperature: float,
        exp_dir: str,
        task_numbers: int,
    ):
        self.model = model
        self.llm = get_llm(
            model=model,
            max_token=max_token,
            provider=provider,
            cfg_path=cfg_path,
            temperature=temperature,
            top_p=top_p,
        )

        self.token_counter = (
            TokenCounterCached(self.llm)
            if TokenCounterCached.is_cache_enabled(self.llm)
            else TokenCounter(self.llm)
        )
        self.exp_dir = Path(exp_dir+f"/{task_numbers}")

    def get_init_prompt_messages(self) -> List[ChatMessage]:
        """Generate initial prompt messages."""
        system_prompt = ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM)

        spec, scenario, testbench,module_header = self.load_input_files()

        init_prompt = ChatMessage(
            content=INIT_EDITION_PROMPT.format(
                spec=spec, scenario_discription=scenario, testbench=testbench,example=example,module_header=module_header
            ),
            role=MessageRole.USER,
        )

        return [system_prompt, init_prompt]

    def get_order_prompt_messages(self) -> List[ChatMessage]:
        """Generate order prompt messages."""
        return [
            ChatMessage(
                    content=ORDER_PROMPT.format(
                        output_format="".join(
                            json.dumps(EXAMPLE_OUTPUT_FORMAT, indent=4)
                        )
                    ),
                    role=MessageRole.USER,
                ),
        ]


    def load_input_files(self) -> Tuple[str, str, str]:
        """Load the spec, scenario description and testbench files."""
        with open(self.exp_dir / "spec.txt", "r") as f:
            spec = f.read()

        with open(self.exp_dir / "TB_scenarios.txt", "r") as f:
            scenario = f.read()

        with open(self.exp_dir / "testbench.json", "r") as f:
            testbench = f.read()
        
        with open(self.exp_dir / "module_header.txt", "r") as f:
            module_header = f.read()

        return spec, scenario, testbench,module_header

    def run(self) -> bool:
        """
        Main function to check consistency and fix implementation if needed.
        Returns True if all scenarios match after potential fixes.
        """
        """Single chat interaction to check consistency."""
        #spec, scenario, testbench = self.load_input_files()
        if isinstance(self.token_counter, TokenCounterCached):
            self.token_counter.set_enable_cache(True)
        self.token_counter.set_cur_tag(self.__class__.__name__)

        # Generate response
        messages = self.get_init_prompt_messages() + self.get_order_prompt_messages()
        logger.info(f"Consistency checker input message: {messages}")
        resp, token_cnt = self.token_counter.count_chat(messages)
        logger.info(f"Token count: {token_cnt}")
        logger.info(f"Response: {resp.message.content}")
        note=""
        #response_content = resp.message.content
        try:
                # output_json_obj: Dict = json.loads(response.message.content, strict=False)

                # use this for Deepseek r1 and claude-3-5-sonnet
                # if self.model == "claude-3-5-sonnet-20241022":
                #     output_json_obj: Dict = json.loads("".join(response.choices[0].message.content.split("\n")[1:]), strict=False)
                # else:
                #     output_json_obj: Dict = json.loads(response.choices[0].message.content, strict=False)
                output_json_obj: Dict = json.loads(resp.message.content, strict=False)
                unmatch_case=0

                print(output_json_obj)
                for data in output_json_obj["result"]:
                    if data["if_matches"] == "no":
                        note+= f"The case {data['name']} does not match the specification\n"
                        note+=f'the reasoning is {data["explanation"]}\n'
                        note+=f'the input variable is {data["input_variable"]}\n'
                        note+= f"The present output is {data['unmatched_present_output']}\n"
                        note+= f"The correct output is {data['correct_output']}\n"
                        unmatch_case+=1
                if unmatch_case>0:
                    logger.error(f"There are {unmatch_case} unmatch cases")
                
                else:
                    logger.info(f"All cases match the specification")
        except json.decoder.JSONDecodeError as e:
                    print(f"Json parse error: {e}")
                    logger.info(f"Json parse error: {e}")
                    print(resp)
                    return None
        print(f"the unmatch case is {unmatch_case}")
        with open(self.exp_dir / "output.txt", "w") as f:
                    f.write(note)

            # Run consistency check again with new implementation
            # Note: You might want to implement a mechanism to use the new file
            # return check_and_fix_implementation(exp_dir, token_counter)

        return unmatch_case



args_dict = {
    # "model": "deepseek-reasoner",
    # "model": "gpt-4o-2024-08-06",
    # "model": "gpt-4o-mini-2024-07-18",
    # "model": "gemini-2.0-flash",
    # "model": "claude-3-5-sonnet-v2@20241022",
    # "model_fixer": "models/gemini-2.0-flash",
    "model": "claude-3-5-sonnet-20241022",
    # "model_fixer": "gpt-4o-2024-08-06",
    # "provider": "anthropic",
    #"provider": "openai",
    "provider": "anthropic",
    # "provider_fixer": "anthropic",
    # "provider_fixer": "openai",
    "temperature": 0,
    "top_p": 1,
    "temperature_sample": 0.3,
    "top_p_sample": 0.95,
    "max_token": 8096,
    # "model": "claude-3-7-sonnet@20250219",
    #"model": "claude-3-5-sonnet-v2@20241022",
    #"provider": "vertexanthropic",
    #"provider": "vertex",
    #"model": "gemini-1.5-flash",
    "provider_fixer": "vertex",
    # "task_numbers": [50],
    "task_numbers": [121,125,130,140,143],
    # "filter_instance": "Prob051|Prob052|Prob053|Prob054|Prob055|Prob101|Prob102|Prob103|Prob104|Prob105",
    # "filter_instance": "Prob092",
    # "filter_instance": "",
    "folder_path": "../verilog-eval/HDLBits/HDLBits_data_backup0304.jsonl",
    "run_identifier": "mismatch_report_for_correctness",
    "key_cfg_path": "../key.cfg",
    "use_golden_ref": True,
    "max_trials": 5,
    "exp_dir": "output_tb_gen_tb_20250406"
}



def main():
    # Example usage
    
    args = argparse.Namespace(**args_dict)
    Config(args.key_cfg_path)
    switch_log_to_file()
    timestamp = datetime.now().strftime("%Y%m%d")
    output_dir = f"{args.run_identifier}_{timestamp}"
    log_dir = f"log_{args.run_identifier}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    results=[]
    incorrect_cases=[46, 55, 56, 59, 63, 78, 86, 94, 98, 99, 107,118, 120, 142, 147, 148,  149, 150, 152, 153]
    not_identify_mistake=[]
    wrong_identify_correct_cases=[]
    summary_txt= ""
    for task_number in args.task_numbers:

        set_log_dir(log_dir)
        
        consistency_checker = ConsistencyChecker(args.model, args.max_token, args.provider, args.key_cfg_path, args.top_p, args.temperature, args.exp_dir, task_number)
        unmatch_case = consistency_checker.run()
        if unmatch_case>0:
            
            summary_txt+= f"There are {unmatch_case} unmatch cases for task {task_number}\n"
        else:
           
            summary_txt+= f"All cases match the specification for task {task_number}\n"
        results.append(unmatch_case)
    
        if unmatch_case>0 and task_number not in incorrect_cases:
            wrong_identify_correct_cases.append(task_number)
        if unmatch_case==0 and task_number in incorrect_cases:
            not_identify_mistake.append(task_number)
    
    with open(f"{args.run_identifier}_summary.txt", "w") as f:
        f.write(summary_txt+str(results)+'\n'+str(not_identify_mistake)+'\n'+str(wrong_identify_correct_cases))
    


    

if __name__ == "__main__":
    main()