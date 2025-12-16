import json
from typing import Dict, List

from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
from .mage.gen_config import get_llm
from .mage.log_utils import get_logger
from .mage.prompts import ORDER_PROMPT
from .mage.token_counter import TokenCounter, TokenCounterCached
from pydantic import BaseModel

logger = get_logger(__name__)

SYSTEM_PROMPT = """
You are an expert in RTL design. You can always write SystemVerilog code with no syntax errors and always reach correct functionality. You can always generate correct testbenches for your RTL designs. Based on this analysis, you must generate detailed testbench scenarios in structured JSON format. Clearly state your reasoning for each scenario.
"""

GENERATION_PROMPT = """
You are tasked with designing test cases for a combinational digital circuit. Your goal is to create comprehensive test cases that thoroughly examine the circuit's functionality under various input combinations. Follow these instructions carefully to design appropriate test cases. Here is the information you have:
1. <description>
{description}
</description>

2. <module_header>
{module_header}
</module_header>

3. <instruction>
{instruction}
</instruction>


<example>
{example}
</example>

Guidelines for designing test cases:

The testbench scenarios should be comprehensive and cover all critical aspects of the circuit's functionality. You must design at least 8 testbench scenarios.

Focus on functional correctness under different input combinations, especially edge cases and boundary conditions.

Since this is a combinational circuit, there is no need to consider clock cycles. All outputs are determined solely by the current inputs.

Describe only the behavior of input signals for each scenario. Do not describe output signals.

Consider a wide range of input patterns, including:

all-zero and all-one inputs

alternating bit patterns

minimum and maximum values (if input is multi-bit)[Important] You must not generate values that described as "never occur", "do not care", "not applicable", or "not required to check", etc.

one-hot or gray code patterns (if applicable)

invalid or unexpected input combinations (if the spec allows)

Your goal is to stress test the circuit's logic coverage and ensure that every logic path is exercised.

The information you have is:

1. The problem description that guides student to write the RTL code (DUT)
2. The header of the "DUT"
3. The instruction for writing the testbench

Analyze its behavior thoroughly and create representative testbench scenarios. Clearly state your reasoning for each scenario. Structure the scenarios as JSON descriptions, ensuring each scenario covers critical aspects, including:
a. Typical operations
b. Timing: Pay attention to the timing relationships between different signals.





Special Instructions for Karnaugh Map-based Circuits:

When analyzing the function from the Karnaugh map, explicitly avoid generating test scenarios for input combinations marked as don't care (d or unspecified in the map). These inputs do not affect functional correctness and should not be interpreted or tested unless they are necessary for minimizing the logic expression.

Focus only on input combinations with defined outputs (0 or 1). Do not describe scenarios involving ambiguous or undefined behavior from the Karnaugh map.

In test case scenario descriptions, clearly explain which variables are being controlled and ensure all variables involved are fully specified.
"""


EXTRA_PROMPT = """

"""

EXAMPLE_OUTPUT = {
    "reasoning": "Analyze the technical specification and infer the test scenarios",
    "test_case": [
        {
            "scenario": "The testbench scenario name, do not include Punctuation!",
            "description": "The description of the testbench scenario",
        }
    ],
}
FEW_SHOT_EXAMPLE = """
Here are some examples of SystemVerilog testbench scenarios descriptions:
Example 1:
<example>
    <input_spec>
       You are given a four-variable Boolean function f(a, b, c, d) represented by the following Karnaugh map. The output values are 1, 0, or d (don't-care). Only test cases corresponding to defined output values (1 or 0) should be used. Do not generate test cases for don't-care entries.
              ab
cd     00  01  11  10
     +-----------------
00 |   1 |  1 |  d |  0 |
01 |   1 |  0 |  0 |  1 |
11 |   d |  0 |  1 |  1 |
10 |   0 |  1 |  1 |  d |

    </input_spec>
    <test_case>
   [
  {
    "scenario": "AllZerosInput",
    "description": "Inputs a, b, c, d are all 0 (0000), which corresponds to a defined output of 1. This tests the function's behavior at its ground state."
  },
  {
    "scenario": "HorizontalScanOnCDRow00",
    "description": "Keep inputs c=0 and d=0 constant. Sweep a and b from 00 to 10 to observe outputs 1, 1, and 0 (skipping the don't-care at ab=11)."
  },
  {
    "scenario": "CornerCaseInput0110",
    "description": "Set inputs a=0, b=1, c=1, d=0 (0110), corresponding to a defined output of 1. This case probes a boundary cell at the lower-left of the Karnaugh map."
  },
  {
    "scenario": "VerticalEdgeTransitionFrom0100to1100",
    "description": "Start at abcd=0100 and transition to abcd=1100. Both points have defined outputs (1 and 1), and the transition avoids don't-care regions."
  },
  {
    "scenario": "MiddleColumnAB01SweepCD",
    "description": "Fix a=0, b=1, and sweep c and d through all values from 00 to 11. The outputs are defined for 0100 (1), 0101 (0), 0110 (0), and 0111 (1)."
  },
  {
    "scenario": "CDFluctuationWithAB10",
    "description": "Fix a=1 and b=0. Vary c and d across valid patterns: 1000 (0), 1010 (1), and 1110 (1). This tests how cd fluctuations affect output at a fixed ab setting."
  },
  {
    "scenario": "DefinedOutputBoundaryNearDontCare",
    "description": "Use input abcd=1110, which is defined as output 1. This cell is adjacent to a don't-care region, ensuring correctness near undefined logic."
  },
  {
    "scenario": "AlternatingBitPatternsWithDefinedOutputs",
    "description": "Use patterns abcd=0101 and abcd=1010. These correspond to defined outputs of 0 and 1, and test the circuit's response to alternating input bits."
  }
]

    
</test_case>
    
Example 2:
<example>
    <input_spec>
        A 4‑bit combinational ALU. Inputs: A[3:0], B[3:0], OPCODE[1:0]. Operations — 00: ADD (A+B, wrap‑around on overflow); 01: SUB (A–B, wrap‑around on underflow); 10: AND (bitwise); 11: OR (bitwise). No flags or clock.",
    </input_spec>

    <test_case>
  {
  "reasoning": "The ALU has four operations and 4‑bit operands, so thorough testing must sweep corner‑case numerical values, overflow/underflow conditions, diverse bit patterns, and an illegal‑opcode edge. Eight scenarios exercise every logic path and boundary condition while describing only input behaviour.",
  "test_case": [
    {
      "scenario": "AllZeroInputs",
      "description": "Drive A = 0000, B = 0000 while sweeping OPCODE through 00,01,10,11 to check neutral behaviour."
    },
    {
      "scenario": "AllOneInputs",
      "description": "Drive A = 1111, B = 1111 with each OPCODE value to test max data path and logical saturation."
    },
    {
      "scenario": "AddOverflowCheck",
      "description": "Set OPCODE = 00 and apply A = 1111, B = 0001 then A = 1000, B = 1000 to observe wrap‑around addition cases."
    },
    {
      "scenario": "SubUnderflowCheck",
      "description": "Set OPCODE = 01 and apply A = 0000, B = 0001 then A = 0111, B = 1000 to exercise wrap‑around subtraction."
    },
    {
      "scenario": "AlternatingBitPatternAnd",
      "description": "Set OPCODE = 10 with A = 1010, B = 0101 to verify AND operation on complementary patterns."
    },
    {
      "scenario": "AlternatingBitPatternOr",
      "description": "Set OPCODE = 11 with the same A = 1010, B = 0101 to verify OR operation merges high bits."
    },
    {
      "scenario": "OneHotOperands",
      "description": "Sweep A through 0001,0010,0100,1000 while holding B = 0000 for each OPCODE to ensure single‑bit paths are correct."
    },
    {
      "scenario": "InvalidOpcodeBehaviour",
      "description": "Force OPCODE = 10 (AND) and 11 (OR) are legal; additionally drive an illegal pattern OPCODE = 1X (where X is Z in simulation) to confirm stable output or defined default handling."
    }
  ]
}


    </test_case>

</example>

Example 3:
<example>
    <input_spec>
        "Moore FSM: Overlapping 3‑bit Sequence Detector for pattern 101.\n• States: S0 (idle), S1 (saw 1), S2 (saw 10).\n• Inputs: clk (posedge‑triggered), areset (active‑high async), x (serial data bit).\n• Output: y = 1 only in state S2 **on the cycle _after_ the full pattern 101 is seen**; otherwise y = 0.\n• If areset = 1 the FSM returns to S0 immediately; y is forced to 0 in S0.\n• Illegal state encoding is self‑correcting to S0 on the next clock.",
    </input_spec>
    <test_case>
    "reasoning": "To verify every state transition and edge case we need scenarios that: (i) exercise the normal detection path, (ii) check overlapping detections, (iii) toggle asynchronous reset from different states, (iv) stress the machine with long runs of identical bits, and (v) probe illegal state recovery. Eight input‑only scenarios, each ≥ 10 cycles, guarantee full coverage.",
  "test_case": [
    {
      "scenario": "IdleAllZeros",
      "description": "Clock 12 cycles with areset = 0 and x held 0 to confirm the FSM stays in S0 and never asserts y."
    },
    {
      "scenario": "SinglePatternDetect",
      "description": "Apply x = 1‑0‑1 followed by seven 0s (total 10 cycles) with areset = 0 to verify one clean 101 detection."
    },
    {
      "scenario": "OverlappingPatterns",
      "description": "Feed bit stream 1‑0‑1‑0‑1‑1‑0‑1 over 12 cycles (areset = 0) to test overlapping recognition producing two adjacent detections."
    },
    {
      "scenario": "LongOnesBurst",
      "description": "Hold x = 1 for 11 cycles then a single 0 while areset = 0 to ensure the FSM does not falsely trigger without the full 101 sequence."
    },
    {
      "scenario": "AsyncResetAtStart",
      "description": "Keep areset = 1 for the first 3 cycles, then de‑assert and supply bit stream 1‑0‑1‑0‑0‑0 over the next 9 cycles to verify proper reset release behaviour."
    },
    {
      "scenario": "AsyncResetMidSequence",
      "description": "Begin a 101 detection, assert areset high for one cycle midway (after bits 1‑0) and continue; total 11 cycles to confirm reset aborts partial progress."
    },
    {
      "scenario": "ContinuousRandomBits",
      "description": "Drive a pseudorandom x sequence (e.g., 1‑1‑0‑1‑0‑0‑1‑0‑1‑1‑0) for 11 cycles with areset = 0 to exercise miscellaneous paths and idle returns."
    },
    {
      "scenario": "IllegalStateRecovery",
      "description": "Force the encoded state lines externally (in simulation) to an undefined value for one cycle while areset = 0, then supply benign x = 0 for 10 cycles to validate automatic return to S0 without assertion of y."
    }
  ]
</example>

"""

class ScenarioItem(BaseModel):
    scenario: str
    description: str


class TBOutputFormat(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    reasoning: str
    test_case: List[ScenarioItem]


class TB_Generator_Scenario_CMB:
    def __init__(
        self,
        model: str,
        max_token: int,
        provider: str,
        cfg_path: str,
        tb_scenarios_path: str,
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
        self.tb_scenarios_path = tb_scenarios_path

    def parse_output(self, response: ChatResponse) -> TBOutputFormat:
        try:
            output_json_obj: Dict = json.loads(response.message.content, strict=False)
            scenarios = output_json_obj["test_case"]
            if isinstance(scenarios, dict):
                scenarios = [scenarios]
            elif not isinstance(scenarios, list):
                scenarios = []

            ret = TBOutputFormat(
                reasoning=output_json_obj["reasoning"], test_case=scenarios
            )
        except json.decoder.JSONDecodeError:
            ret = TBOutputFormat(reasoning="", test_case=[])
        return ret

    def generate(self, messages: List[ChatMessage]) -> ChatResponse:
        logger.info(f" input message: {messages}")
        resp, token_cnt = self.token_counter.count_chat(messages)
        logger.info(f"Token count: {token_cnt}")
        logger.info(f"{resp.message.content}")
        return resp

    def run(self, input_spec: str, header: str, circuit_type: str = "SEQ") -> str:
        msg = [
            ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
            ChatMessage(
                content=GENERATION_PROMPT.format(
                    description=input_spec,
                    module_header=header,
                    example=FEW_SHOT_EXAMPLE,
                    instruction=EXTRA_PROMPT,
                ),
                role=MessageRole.USER,
            ),
            ChatMessage(
                content=EXTRA_PROMPT,
                role=MessageRole.USER,
            ),
        ]
        if circuit_type == "SEQ":
            msg.append(ChatMessage(content=EXTRA_PROMPT, role=MessageRole.USER))
            
        msg.append(
            ChatMessage(
                content=ORDER_PROMPT.format(
                    output_format="".join(json.dumps(EXAMPLE_OUTPUT, indent=4))
                ),
                role=MessageRole.USER,
            )
        )

        response = self.generate(msg)
        tb_scenarios = self.parse_output(response).test_case

        # Convert list to formatted string
        scenarios_str = ""
        for scenario in tb_scenarios:
            scenarios_str += f"scenario: {scenario.scenario}\n"
            scenarios_str += f"description: {scenario.description}\n\n"

        # Write to file
        with open(self.tb_scenarios_path, "w") as f:
            f.write(scenarios_str)

        logger.info(f"Get response from {self.model}: {response}")

        return scenarios_str  # Return string instead of list
