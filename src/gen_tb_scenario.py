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
You are tasked with designing test cases for a digital circuit. Your goal is to create comprehensive test cases that thoroughly examine the circuit's functionality. Follow these instructions carefully to design appropriate test cases.
Guidelines for designing test cases:
- The testbench scenarios should be comprehensive and cover all critical aspects of the circuit's functionality. So the number of testbench scenarios should be at least 8.
- Focus on testing the circuit's functionality
- Use a relatively long number of clock cycles (typically more than 10) to ensure thorough testing
- Describe only the behavior of input signals, not output signals
- Consider various scenarios that could affect the circuit's operation. It is the most important to consider.

The information you have is:

1. The problem description that guides student to write the RTL code (DUT)
2. The header of the "DUT"
3. The instruction for writing the testbench

Analyze its behavior thoroughly and create representative testbench scenarios. Clearly state your reasoning for each scenario. Structure the scenarios as JSON descriptions, ensuring each scenario covers critical aspects, including:
a. Typical operations
b. Timing: Pay attention to the timing relationships between different signals.

[Important] You must not generate testbench stimuli scenarios that are labeled as "never occur", "do not care", "not applicable", or "not required to check", etc.



Here is the information you have:
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
        Implement an 8-bit synchronous up-counter with:
        - Clock (clk) rising-edge triggered
        - Active-high asynchronous reset (RST)
        - Active-high enable (EN)
        - Output value wraps from 255 to 0 on overflow
    </input_spec>

    <test_case>
  "test_case": [
    {
        "scenario": "ConstantLowInput",
        "description": "10 clock cycles. Input a is held at 0 for 10 clock cycles to verify that q remains 0 after each rising edge."
    },
    {
        "scenario": "ConstantHighInput",
        "description": "10 clock cycles. Input a is held at 1 for 10 clock cycles to verify that q is consistently set to 1 on each rising edge."
    },
    {
        "scenario": "SinglePulseLowToHigh",
        "description": "10 clock cycles. Input a starts at 0, then changes to 1 for a single cycle at the 5th clock, then returns to 0 to verify a single rising edge change is captured."
    },
    {
        "scenario": "AlternatingInputPattern",
        "description": "12 clock cycles. Input a alternates between 0 and 1 every clock cycle over 12 cycles to test that q follows the toggling input on each rising edge."
    },
    {
        "scenario": "RandomLikePattern",
        "description": "16 clock cycles. Input a changes in a non-repeating pattern over 16 clock cycles to simulate realistic signal fluctuations and validate correct sampling behavior."
    },
    {
        "scenario": "DelayedChangeAfterReset",
        "description": "16 clock cycles. Input a is held at 0 for the first 4 clock cycles, then toggles between 1 and 0 every 2 cycles to test stability before transition."
    },
    {
        "scenario": "GlitchResistantCheck",
        "description": "16 clock cycles. Input a toggles rapidly but only changes on falling edges to ensure that q only changes value on rising clock edges, not on glitchy transitions."
    }
]


    </test_case>
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


class TB_Generator_Scenario:
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
