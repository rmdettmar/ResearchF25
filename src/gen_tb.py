import json
import base64
from typing import Dict, List

from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
from .gen_config import get_llm
from .log_utils import get_logger
from .prompts import ORDER_PROMPT
from .token_counter import TokenCounter, TokenCounterCached
from pydantic import BaseModel
from . import python_call as py
logger = get_logger(__name__)

SYSTEM_PROMPT = """
You are an expert in RTL design. You can always write SystemVerilog code with no syntax errors and always reach correct functionality. You can always generate correct testbenches for your RTL designs.
"""

GENERATION_PROMPT = """
Your task is to generate Python method named "stimulus_gen" to produce a list of Dictionary-formatted stimulus sequences for testing a given DUT (Device Under Test). If necessary, write any additional methods that may be called within the load method to organize the code and handle specific sub-tasks. The information you have is:

1. The problem description that guides student to write the RTL code (DUT)
2. The header of the "DUT"
3. The instruction for writing the testbench
4. The list of testbench scenarios description

The object of the stimulus list format should strictly follow the dictionary structure below:
{{
  "scenario": "scenario_name1",
  "input variable": [
    {{"variable_name": variable_value}},
    {{"variable_name": variable_value}},
    {{"variable_name": variable_value}}
  ]
}}

Each input variable sequence should be customized based on the given specific scenario description, typically including:

a. Typical operations
b. Edge cases and corner cases
c. Boundary conditions
d. Error handling
e. Random cases as much as possible
f. Timing verification requirements

Please follow these steps:

1. First, analyze the given test scenarios description.

2. Generate Python method named "stimulus_gen" follow the instruction:
<instruction>
{instruction}
</instruction>



Here is the information you have:
1. <description>
{description}
</description>

2. <module_header>
{module_header}
</module_header>

3. <test_scenarios>
{test_case}
</test_scenarios>



3. If spec does not have invalid input, you can generate more than 20 random test cases using python loop. It is a good way to cover all the possible cases.
Each input variable sequence should be customized based on the given specific scenario description, typically including:

a. Typical operations
b. Edge cases and corner cases
c. Boundary conditions
d. Error handling
e. Random cases (it is based on the input variable are all valid, then you can use loop to generate at least 10 cases )
f. Timing verification requirements

Please generate the testbench following the format in the example below:
<example>
{example}
</example>
"""

Instructions_for_Python_Code = """
[important]Instructions for the Python Code:
0.[Most importantly] Every variable (signal) must be represented explicitly as a binary sequence (e.g., '101001'). Only binary digits '0' and '1' are allowed; do NOT include any undefined ('X') or high-impedance ('Z') states.
1. The output should be a list of dictionaries, each dictionary is a stimulus sequence following the format:{{
  "scenario": "scenario_name",
  "input variable": [
    {{"variable_name1": (a binary sequence string)variable_value1,
    "variable_name2": (a binary sequence string)variable_value2,
    "variable_name3": (a binary sequence string)variable_value3}},
    {{"variable_name1": (a binary sequence string)variable_value1,
    "variable_name2": (a binary sequence string)variable_value2,
    "variable_name3": (a binary sequence string)variable_value3}}

  ]}}
[important]The variable names in the "input variable" should include all the input variables in the DUT module header.
3 . Carefully read and interpret each description in the list of testbench scenarios. Write a Python method named stimulus_gen that returns a list of dictionary-formatted stimulus sequences. Ensure the length of the generated list matches exactly the number of provided testbench scenarios.
5. The stimulus_gen method can call and rely on any additional helper methods or sub-methods as needed to generate the stimulus sequences clearly and efficiently.
6. Clearly define and document any helper methods that you use.


[Some hints for combinational circuits]
0. For combinational circuits specifically:
   - Ensure each test vector specifies a complete set of input values
   - For exhaustive testing, consider generating all possible input combinations when feasible
   - For targeted testing, focus on edge cases and boundary conditions
   - Remember that unlike sequential circuits, combinational circuits have no memory or state
1. Truth Table Exploration: Consider generating stimuli that cover the entire truth table for small input spaces, or use strategic input selection for larger spaces.

2. Special Cases: Pay special attention to:
   - All zeros/all ones inputs
   - Alternating bit patterns (101010...)
   - Single bit changes (walking ones/zeros)
   - Corner cases specific to the circuit functionality

3. Techniques for Generating Binary Values in Python:
   - Integer conversion: format(42, '08b')  # '00101010'
   - Bitwise operations: format((1 << 3) | (1 << 0), '08b')  # '00001001'
   - Systematic patterns: format((2**i), f'0{width}b') for i in range(width)
4. When handling inputs containing Karnaugh maps, 01 sequences, or logic diagrams: Recognize that Karnaugh map columns often follow Gray code ordering (00, 01, 11, 10). Always convert outputs to standard binary sequence (00, 01, 10, 11) unless explicitly instructed otherwise. Example: If input columns are [00, 01, 11, 10], process/output using [00, 01, 10, 11] ordering.

Perform bitwise consistency checks for all 01 sequences: Confirm input/output bit lengths match. Verify no duplicate minterms in truth tables. Cross-check Karnaugh map groupings against standard adjacency rules.

When detecting non-standard ordering in inputs, check the order of outputs.
Remember that for combinational circuits, there is no concept of clock cycles or sequential behavior - the output is purely a function of the current inputs.

[Return Value Format]
The stimulus_gen function should either:
1. Return a JSON-formatted string directly, or
2. Return a list/dictionary that can be JSON serialized




Special Instructions for Karnaugh Map-based Circuits:

When analyzing the function from the Karnaugh map, !!!explicitly avoid generating test scenarios for input combinations marked as don't care (d or unspecified in the map). These inputs do not affect functional correctness and should not be interpreted or tested unless they are necessary for minimizing the logic expression.

!!! Focus only on input combinations with defined outputs (0 or 1). Do not describe scenarios involving ambiguous or undefined behavior from the Karnaugh map.

In test case scenario descriptions, clearly explain which variables are being controlled and ensure all variables involved are fully specified.

[Return Value Format]
The stimulus_gen function should either:
1. Return a JSON-formatted string directly, or
2. Return a list/dictionary that can be JSON serialized
The function's output will be automatically converted to a JSON string before writing to file.

[important]The variable names in the "input variable" should include all the input variables, including reset signal(rst or areset) in the DUT module header, except the clock signal(clk).

Follow these steps to create the stimulus_gen method:

1. Analyze the inputs:
   - Extract the input variable names from the DUT header
   - Identify the required scenarios from the testbench scenarios

2. Create the stimulus_gen method structure:
   - Define the method signature: def stimulus_gen()
   - Initialize an empty list to store the stimulus sequences

3. Process each scenario:
   - For each scenario in the testbench scenarios:
     a. Create a dictionary with the scenario name
     b. Create a list of input dictionaries for each set of input variables
     c. For each set of input variables:
        - Create a dictionary with "clock cycles" and input variable names as keys
        - Generate binary sequence strings for each input variable based on the number of clock cycles
     d. Add the input list to the scenario dictionary
     e. Append the scenario dictionary to the main stimulus list

4. Handle error cases and edge conditions:
   - Ensure that the number of binary sequence strings matches the specified clock cycles
   - Validate that all required input variables are present
   - Handle any potential errors gracefully

Remember to follow Python best practices, use meaningful variable names, and include comments to explain your code.

Important notes:
- Pay close attention to the functionality described in the problem description and testbench instruction.
- Ensure that your method can handle various scenarios and input combinations.
- The cycle time for each scenario is typically longer than 10 clock cycles, so plan your binary sequence generation accordingly.
- Focus more on exploring and implementing the required functionality rather than spending too much time on initial setup or probing.


6. Ensure and ensure the length of the generated list matches exactly the number of provided testbench scenarios.
7. The stimulus_gen method can call and rely on any additional helper methods or sub-methods as needed to generate the stimulus sequences clearly and efficiently.
8. Clearly define and document any helper methods that you use.
9. You must not generate testbench stimuli that are labeled as "never occur", "do not care", "not applicable", or "not required to check", etc.


[Some hints]
1. Input Variable Conformance: Ensure all input variables in the stimulus sequence strictly conform to the DUT module header definition (variable names, bit widths, data types). Clearly indicate variable types (binary, integer, etc.) and bit widths according to the DUT module header.

2 Code Clarity and Maintainability: Clearly document each step and scenario in comments.Consider edge cases involving timing and synchronization relevant to the RTL module's operation.

### 3. Techniques for Generating Binary Stimulus Strings in Python

When working with RTL simulation and verification, generating appropriate binary stimulus sequences is crucial. Here are several Python-based techniques you can use to generate such sequences efficiently:

#### 3.1. Integer-to-Binary Conversion for Functional Testing
For deterministic logic testing, you can convert integers to binary strings. This is useful when you need predictable patterns for verification.

```python
# Convert integer to binary string with zero-padding to fixed width
stimulus = format(42, '08b')  # Output: '00101010'
```

You can use this to systematically generate all combinations for a given bit width:

```python
width = 4
stimuli = [format(i, f'0{width}b') for i in range(2**width)]
```

#### 3.2. Random Binary Sequences
For more stochastic testing, Python's `random` module provides convenient tools:

```python
import random

# Generate a random 32-bit binary string
in = format(random.getrandbits(32), '032b')
```

Or, to generate a list of such random binary strings:

```python
x=16
in=format(x, '04b')   # Convert x to a 4-bit binary string
```

#### 3.3. Custom-Length Random Sequences
You can generate arbitrarily long binary strings using list comprehension and `join`:

```python
# Generate a 1000-bit random binary string
in = ''.join([str(random.randint(0, 1)) for _ in range(1000)])
```

This approach is flexible and allows for insertion of patterns or controlled distributions.

```


```


4. Specific Recommendations for stimulus_gen Module:

Leverage Python loops (for, while) to efficiently generate repetitive or sequential test inputs. Use parameterized functions or loops to cover various input ranges and boundary conditions systematically. Ensure scalability by avoiding hard-coded scenarios; instead, use loop-driven generation for comprehensive coverage.

[Return Value Format]
The stimulus_gen function should either:
1. Return a JSON-formatted string directly, or
2. Return a list/dictionary that can be JSON serialized
The function's output will be automatically converted to a JSON string before writing to file.
"""

EXTRA_PROMPT_SEQ = """

"""
python_code_header = """
import json
import random
"""
EXAMPLE_OUTPUT = {
    "reasoning": "Analyze the scenario description and think how to generate the stimulus sequence",
    "stimulus_gen_code": "python code to generate stimulus sequence",
}
ONE_SHOT_EXAMPLE = """
Here are some examples of SystemVerilog testbench code:
Example 1:
<input_spec>
    <description>
  For the following Karnaugh map, implement the Boolean function using exactly one 4-to-1 multiplexer and as few 2-to-1 multiplexers as needed. You are not allowed to use any other logic gates. Use variables a and b as the selector inputs for the 4-to-1 multiplexer, as shown in the diagram below.

        // ab
// cd 00 01 11 10
// 00 | 1 | 0 | 1 | 1 |
// 01 | d | d | 0 | 1 |
// 11 | 1 | d | 0 | 0 |
// 10 | 1 | 0 | d | 0 |

Your task is to write RTL code to implement this function using the given constraints. All inputs (a, b, c, d) are Boolean (0 or 1), and the circuit is purely combinational.


    </description>
</input_spec>
<python_code>


def stimulus_gen():

    #Generate stimulus sequences for testing the DUT based on predefined Karnaugh-map scenarios.

    # Define the input patterns for each scenario (a, b, c, d in that order)
    # Since abcd=0000, 0101, 1111,1 110 is the don't care input, we don't need to generate it
    scenario_patterns = {
        "FIRSTVALIDINPUT": ["0000"],
        "SECONDVALIDINPUT": ["0001"],
        "THIRDVALIDINPUT": ["0010"],
        "FOURTHVALIDINPUT": ["0011"],
        "FIFTHVALIDINPUT": ["0100"],
        "SIXTHVALIDINPUT": ["0101"],
        "SEVENTHVALIDINPUT": ["0110"],
        "EIGHTHVALIDINPUT": ["0111"],
        "NINTHVALIDINPUT": ["1000"],
        "TENTHVALIDINPUT": ["1001"],
        "ELEVENTHVALIDINPUT": ["1010"],
        "TWELFTHVALIDINPUT": ["1011"],
        "THIRTEENTHVALIDINPUT": ["1100"],
        "FOURTEENTHVALIDINPUT": ["1101"],
        "FIFTEENTHVALIDINPUT": ["1110"],
        "SIXTEENTHVALIDINPUT": ["1111"],
    }

    stimuli = []
    for scenario, patterns in scenario_patterns.items():
        input_list = []
        for bits in patterns:
            # Decompose the 4-bit string into individual signals
            input_vars = {
                "a": bits[0],
                "b": bits[1],
                "c": bits[2],
                "d": bits[3]
            }
            input_list.append(input_vars)
        stimuli.append({
            "scenario": scenario,
            "input variable": input_list
        })

    return stimuli


# Example usage:
if __name__ == "__main__":
    for stimulus in stimulus_gen():
        print(stimulus)

</python_code>

Example 2:
<example>
    <input_spec>
       Implement the boolean function z = (x|y) & (~x).
    </input_spec>

    <stimulus_gen_code>
   def stimulus_gen() -> list[dict]:
    scenarios = [
        {
            "scenario": "AllZeroInputs",
            "input variable": [{"x": "0", "y": "0"}]
        },
        {
            "scenario": "AllOneInputs",
            "input variable": [{"x": "1", "y": "1"}]
        },
        {
            "scenario": "InputXOnlyHigh",
            "input variable": [{"x": "1", "y": "0"}]
        },
        {
            "scenario": "InputYOnlyHigh",
            "input variable": [{"x": "0", "y": "1"}]
        },
        {
            "scenario": "ToggleXKeepYLow",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "1", "y": "0"},
                {"x": "0", "y": "0"},
                {"x": "1", "y": "0"}
            ]
        },
        {
            "scenario": "KeepXLowToggleY",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "0", "y": "1"},
                {"x": "0", "y": "0"},
                {"x": "0", "y": "1"}
            ]
        },
        {
            "scenario": "ToggleXKeepYHigh",
            "input variable": [
                {"x": "0", "y": "1"},
                {"x": "1", "y": "1"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "1"}
            ]
        },
        {
            "scenario": "ComplexSequence",
            "input variable": [
                {"x": "0", "y": "0"},
                {"x": "0", "y": "1"},
                {"x": "1", "y": "0"},
                {"x": "1", "y": "1"},
                {"x": "0", "y": "1"}
            ]
        }
    ]
    return scenarios

</stimulus_gen_code>
</example>
"""
tail = """
if __name__ == "__main__":
    result = stimulus_gen()
    # Convert result to JSON string
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
"""


class TBOutputFormat(BaseModel):
    reasoning: str
    stimulus_gen_code: str


class TB_Generator:
    def __init__(
        self,
        model: str,
        max_token: int,
        provider: str,
        cfg_path: str,
        stimulus_python_path: str,
        temperature: float,
        top_p: float,
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

        self.stimulus_python_path = stimulus_python_path

    def parse_output(self, response: ChatResponse) -> TBOutputFormat:
        try:
            output_json_obj: Dict = json.loads(response.message.content, strict=False)
            ret = TBOutputFormat(
                reasoning=output_json_obj["reasoning"],
                stimulus_gen_code=output_json_obj["stimulus_gen_code"],
            )
            return ret
        except json.decoder.JSONDecodeError:
            return TBOutputFormat(reasoning="", stimulus_gen_code="")

    def generate(self, messages: List[ChatMessage]) -> ChatResponse:
        logger.info(f" input message: {messages}")
        resp, token_cnt = self.token_counter.count_chat(messages)
        logger.info(f"Token count: {token_cnt}")
        logger.info(f"{resp.message.content}")
        return resp

    def run(
        self,
        input_spec: str,
        header: str,
        tb_scenario_description: str,
        circuit_type: str = "SEQ",
        stimuli_sampling_size: int = 3,
        scenarios_filetype: str = "txt",
    ) -> str:
        for i in range(stimuli_sampling_size):

            scenarios = tb_scenario_description
            # if scenarios_filetype == "png":
            #     with open(tb_scenario_description, "rb") as f:
            #         encoded = base64.b64encode(f.read()).decode()
            #         scenarios = f"data:image/png;base64,{encoded}"
            # this only works if the model is image capable (gpt-4o is)

            msg = [
                ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
                ChatMessage(
                    content=GENERATION_PROMPT.format(
                        description=input_spec,
                        module_header=header,
                        example=ONE_SHOT_EXAMPLE,
                        instruction=Instructions_for_Python_Code,
                        test_case=scenarios,
                    ),
                    role=MessageRole.USER,
                ),
            ]
            if circuit_type == "SEQ":
                msg.append(ChatMessage(content=EXTRA_PROMPT_SEQ, role=MessageRole.USER))
            msg.append(
                ChatMessage(
                    content=ORDER_PROMPT.format(
                        output_format="".join(json.dumps(EXAMPLE_OUTPUT, indent=4))
                    ),
                    role=MessageRole.USER,
                )
            )

            response = self.generate(msg)
            # Ensure necessary imports are added before generating code
            stimulus_py_code = (
                python_code_header+ "\n" + self.parse_output(response).stimulus_gen_code + tail
            )
            sampling_stimulus_python_path = self.stimulus_python_path+".py"
            with open(sampling_stimulus_python_path, "w") as f:
                f.write(stimulus_py_code)
                
            stimulus_result = py.python_call_and_save(
                f"{sampling_stimulus_python_path}", silent=True
            )

            logger.info(f"Get response from {self.model}: {response}")
        return stimulus_result
