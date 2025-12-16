import json
from typing import Dict

from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
from .mage.gen_config import get_llm
from .mage.log_utils import get_logger
from .mage.prompts import ORDER_PROMPT
from .mage.token_counter import TokenCounter, TokenCounterCached
from pydantic import BaseModel

logger = get_logger(__name__)

SYSTEM_PROMPT = """You are an expert in RTL design and C++ programming. You can always write correct C++ code to verify sequential RTL functionality. You should realize a function in verilator's sim_main.cpp to verify the sequential RTL design."""

GENERATION_PROMPT = """
Your task is to implement a C++ test function named **test_top** that will verify the functionality described in the natural language specification description. The test function should:

1. The input parameters must be carefully declared to match the module interface:
   - For combinational circuits, all module inputs and outputs should be included. Output parameters must be passed by reference; For sequential circuits: Include clk, rst, and all other inputs/outputs. So the total count of input parameters should be the same as the total count claimed in the top module header. Output parameters must be passed by reference, e.g., for module top(input clk, input rst, input load, input [1:0] din, output [1:0] dout);, the input parameters should be void test_top(bool clk, bool rst, bool load, uint8_t data_in, uint8_t &data_out);
   - Ensure parameter lengths match module port widths exactly
   - Use appropriate C++ data types based on signal widths
   - Handle both single-bit and multi-bit signals correctly

2. State variable handling:
   - Declare state variables for all internal registers
   - Initialize state variables to proper reset values
   - Track previous values of outputs when needed
   - Use appropriate bit widths for all state storage

3. Calculate expected outputs based on:
   - Current input values
   - Current state values
   - Previous state/output values if needed
   - Module specification rules

4. Return all expected outputs in the correct format:
   - Match output port widths exactly
   - Handle both single and multi-bit outputs
   - Ensure proper bit masking for width matching

{code_context}

Information for your implementation:

<description>
{description}
</description>

<module_header>
{module_header}
</module_header>

## Implementation Requirements:

### 1. State Variables Declaration
- Declare the function input definition according to the module header
- Each state variable must:
  * Match the exact bit width of the module header
  * Use appropriate C++ data type (uint8_t, uint16_t, uint32_t, etc.)
  * Be initialized to match RTL reset values
  * Include clear comments describing its purpose
- For arrays/memories, declare with matching dimensions
- Group related state variables together

### 2. Test Function Implementation
Implement a test function that:
- Takes input parameters matching module inputs
- Updates internal states based on inputs
- Calculates expected outputs
- Returns expected outputs for verification

### 3. Helper Functions (optional)
You may implement additional helper functions if needed to organize your code clearly.

## Important RTL-to-C++ Simulation Considerations:

To accurately replicate RTL behavior in C++, explicitly handle the following:

<instructions>
{instructions}
</instructions>
---

C++ implementation examples:

{examples_prompt}
"""

instructions = """
# Simulating RTL Logic with C++: Tips and Examples

## 1. Converting Between Binary and Integer

```cpp
// Binary to integer using bitwise operations
uint32_t binary_to_int(const std::string& bin_str) {
    uint32_t value = 0;
    for(char c : bin_str) {
        value = (value << 1) | (c - '0');
    }
    return value;
}

// Integer to binary string with fixed width
std::string int_to_binary(uint32_t value, int width) {
    std::string result;
    for(int i = width-1; i >= 0; i--) {
        result += ((value >> i) & 1) ? '1' : '0';
    }
    return result;
}

// Masking to fixed width
uint32_t mask_to_width(uint32_t value, int width) {
    return value & ((1 << width) - 1);
}
```

## 2. Basic Logic Operations

```cpp
// Bitwise operations
uint32_t a = 0b1010;
uint32_t b = 0b1100;

uint32_t and_result = a & b;
uint32_t or_result  = a | b;
uint32_t xor_result = a ^ b;
uint32_t not_result = ~a & 0xF; // For 4-bit value
```

## 3. Shifting and Rotations

```cpp
// Shift operations
uint32_t left_shift(uint32_t value, int shift, int width) {
    return (value << shift) & ((1 << width) - 1);
}

uint32_t right_shift(uint32_t value, int shift) {
    return value >> shift;
}

// Rotate operations
uint32_t rotate_left(uint32_t value, int shift, int width) {
    uint32_t mask = (1 << width) - 1;
    return ((value << shift) & mask) | (value >> (width - shift));
}
```

## 4. Sequential Logic

```cpp
class DFlipFlop {
private:
    uint32_t q;
    int width;
    
public:
    DFlipFlop(int w) : width(w), q(0) {}
    
    void update(uint32_t d) {
        q = d & ((1 << width) - 1);
    }
    
    uint32_t get() const { return q; }
};
```

## 5. State Machine Example

```cpp
class SimpleFSM {
private:
    uint32_t state;
    
public:
    SimpleFSM() : state(0) {}
    
    uint32_t tick(bool input_signal) {
        if (state == 0 && input_signal) {
            state = 1;
        }
        else if (state == 1 && !input_signal) {
            state = 0;
        }
        return state;
    }
};
```

## 6. Handling Signed Numbers

```cpp
// Convert two's complement to signed int
int32_t twos_complement_to_int(uint32_t value, int width) {
    int32_t mask = 1 << (width - 1);
    int32_t result = value;
    if (value & mask) {
        result = value - (1 << width);
    }
    return result;
}

// Convert signed int to two's complement
uint32_t int_to_twos_complement(int32_t value, int width) {
    uint32_t mask = (1 << width) - 1;
    return value & mask;
}
```

## Summary
- Use proper masking for fixed-width operations
- Handle signed/unsigned conversions carefully
- Implement sequential logic with clear state management
- Use helper functions for common operations
"""

EXAMPLE_OUTPUT_FORMAT = {
    "reasoning": "All reasoning steps and advice to generate the C++ test function",
    "cpp_code": "The C++ code of the test function"
}

cppHeader = """"""
cppTail = """"""
code_context = """


"""

ONE_SHOT_EXAMPLES = r"""
Here are some examples of the test function generation:
Example 1:

<example>
    <input_spec>

The design is a 2-bit adder that takes two 2-bit inputs (inA and inB) and produces a 3-bit sum (outSUM). The sum should be inA + inB, ignoring any overflow beyond 3 bits.

    </input_spec>
    <module_header>
    module top(
    input  [1:0] inA,
    input  [1:0] inB,
    output [2:0] outSUM
);
    </module_header>
    <cpp_code>
    void test_top(uint8_t inA, uint8_t inB, uint8_t &outSUM) {
    // 1. Set the inputs on the Verilog module
    top->inA = inA & 0x3;  // mask to 2 bits
    top->inB = inB & 0x3;  // mask to 2 bits

    // 2. Calculate the expected result based on the specification
    int expected = (inA + inB) & 0x7; // 3 bits for outSUM

    outSUM = expected;
}

    </cpp_code>
</example>

Example 2:

<example>
    <input_spec>

The design is a small "increment-if-enabled" module. The 2-bit input din is passed to the 2-bit output dout directly unless the 1-bit enable en is high, in which case dout should be din + 1 (only 2 bits of the result are used, effectively discarding higher bits).

    </input_spec>
    <module_header>
    module top(
    input  [1:0] din,
    input        en,
    output [1:0] dout
);
    </module_header>
    <cpp_code>
    void test_top(uint8_t din, bool en, uint8_t &dout) {
    // 1. Set the inputs
    top->din = din & 0x3; // mask to 2 bits
    top->en  = en;

    // 2. Calculate expected output
    // If enable is high, increment din by 1 (mod 4). Otherwise, pass din.
    int expected = en ? ((din + 1) & 0x3) : (din & 0x3);

    dout = expected;
}
    </cpp_code>
</example>

Example 3:

<example>
    <input_spec>
    We have a simple sequential circuit called **simple_seq** with the following behavior: 1. It has a 4-bit input **data_in** and a load signal **load**. 2. On every rising edge of **clk**: - If **rst** is asserted (i.e., rst = 1), the output **data_out** is reset to 0, and **done** is set to 0. - Otherwise, if **load** is high, **data_out** is loaded with **data_in**, and **done** is set to 1 during that cycle. - Otherwise, if **load** is low, **data_out** is incremented by 1, and **done** remains 0.
    </input_spec>
    <module_header>
    module top(
    input  [3:0] data_in,
    input        load,
    input        clk,
    input        rst,
    output [3:0] data_out,  
    output       done
);
    </module_header>
    <cpp_code>
    void test_top(
    bool clk,
    bool rst,
    bool load,
    uint8_t data_in,
    uint8_t &actual_data_out,
    bool &actual_done,

) {
    // Compute expected outputs
    uint8_t expected_data_out;
    bool    expected_done;

    if (rst) {
        // If reset is active, data_out should become 0, done = 0
        expected_data_out = 0;
        expected_done     = false;
    } else if (load) {
        // If load is asserted, data_out = data_in, done = 1
        expected_data_out = data_in;
        expected_done     = true;
    } else {
        // Otherwise, increment the previous data_out, done = 0
        expected_data_out = expected_data_out + 1;
        expected_done     = false;
    }

    // 3. Return the expected outputs
    actual_data_out = expected_data_out;
    actual_done     = expected_done;
}
    </cpp_code>
</example>  
"""

class CppOutputFormat(BaseModel):
    reasoning: str
    cpp_code: str

class CppChecker_SEQ:
    def __init__(
        self,
        model: str,
        max_token: int,
        provider: str,
        cfg_path: str,
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

    def reset(self):
        self.history = []

    def parse_output(self, response: ChatResponse) -> CppOutputFormat:
        try:
            output_json_obj: Dict = json.loads(response.message.content, strict=False)
            ret = CppOutputFormat(
                reasoning=output_json_obj["reasoning"],
                cpp_code=output_json_obj["cpp_code"],
            )
        except json.decoder.JSONDecodeError as e:
            ret = CppOutputFormat(
                reasoning=f"Json Decode Error: {str(e)}", cpp_code=""
            )
        return ret

    def run(
        self,
        problem_description: str,
        header: str,
        cpp_path: str,
        circuit_type: str = "SEQ",
    ) -> str:
        """Generate C++ checker code for the given problem

        Args:
            problem_description: Problem description text
            header: Module header text
            cpp_path: Path to output C++ file
            circuit_type: Circuit type (default: "SEQ")

        Returns:
            Tuple[bool, str]: (success, generated code)
        """
        Code_Context = code_context.format(
            CppHeader=cppHeader,
            CHECKER_TAIL=cppTail,
        )
        prompt = GENERATION_PROMPT.format(
            description=problem_description,
            module_header=header,
            instructions=instructions,
            examples_prompt=ONE_SHOT_EXAMPLES,
            code_context=Code_Context,
        )

        messages = [
            ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
            ChatMessage(content=prompt, role=MessageRole.USER),
            ChatMessage(
                content=ORDER_PROMPT.format(
                    output_format="".join(json.dumps(EXAMPLE_OUTPUT_FORMAT, indent=4))
                ),
                role=MessageRole.USER,
            ),
        ]

        response, token_cnt = self.token_counter.count_chat(messages)
        cpp_output = (
            cppHeader + "\n" + self.parse_output(response).cpp_code + cppTail
        )

        logger.info(f"Token count: {token_cnt}")
        logger.info(f"Response: {response.message.content}")

        with open(cpp_path, "w") as f:
            f.write(cpp_output)

        return True, cpp_output
