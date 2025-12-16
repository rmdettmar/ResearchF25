import json
import os
from typing import Dict, List

from llama_index.core.base.llms.types import ChatMessage, ChatResponse, MessageRole
from src.mage.gen_config import get_llm
from src.mage.log_utils import get_logger
from src.mage.prompts import ORDER_PROMPT
from src.mage.token_counter import TokenCounter, TokenCounterCached
from pydantic import BaseModel

logger = get_logger(__name__)

SYSTEM_PROMPT = """
You are an expert in RTL design. You can always write SystemVerilog code with no syntax errors and always reach correct functionality. You can always generate correct testbenches for your RTL designs. Based on this analysis, you must insert minor functional modifications to a golden SystemVerilog module in order to check a testbench's completeness. Clearly state your reasoning for each inserted bug.
"""

GENERATION_PROMPT = """
You are tasked with inserting minor functional bugs into a digital circuit. Your goal is to create a comprehensive set of mutants that cover many common bugs that occur when writing RTL.
Guidelines for designing bugs:
- Each module should exhibit slightly different and slightly incorrect behavior. The incorrectness may be evident in as few as one edge case.
- The header (module name, input and output signals) should be unmodified in all mutants, EXCEPT the module name, which should always be top_module regardless of the original name.
- The buggy module should be syntactically valid. There should be no comments in the text of the module.
- You should generate exactly four mutants from a single golden module.

The information you have is:
1. The operation of the correct SystemVerilog module
2. The format of the output

Analyze its behavior and consider mistakes that a human engineer may make while writing RTL. Clearly state your reasoning for each inserted bug. Clearly state the modification that has been made. Structure the response as a JSON consisting of reasoning and the complete, syntactically correct SystemVerilog modules.

Here is the information you have:
1. <module>
{module}
</module>

2. <output>
{format}
</output>

<example>
{example}
</example>
"""

EXAMPLE_OUTPUT = {
    "reasoning": "Analyze the module and decide on common bugs which may occur while writing RTL",
    "mutants": [
        {
            "bug": "A description of the inserted bug",
            "module": "SystemVerilog module mutant"
        }
    ],
}
FEW_SHOT_EXAMPLE = """
Here are some examples of minor inserted bugs in a functional SystemVerilog module:
Example 1:
<example>
    <golden_module>
        module RefModule (
            input [31:0] in,
            output [31:0] out
        );

            assign out = {in[7:0], in[15:8], in[23:16], in[31:24]};

        endmodule
    </golden_module>

    <mutants>
    "mutants": [
        {
            "bug": "byte chunks are shifted by one bit before reassembly",
            "module": "module top_module (input [31:0] in, output [31:0] out); assign out = { {in[7:1], 1'b0}, {in[15:9], in[8]}, {in[23:17], in[16]}, {in[31:25], in[24]} }; endmodule
        },
        {
            "bug": "in[23:16] is duplicated, in[7:0] is never used",
            "module": "module top_module (input [32:0] in, output [31:0] out); assign out = { in[23:16], in[15:8], in[23:16], in[31:24] }; endmodule"
        },
        {
            "bug": "for aligned inputs, top byte is wrong (uses b1 instead of b0)"
            "module": "module top_module (input [31:0] in,output [31:0] out); wire [7:0] b0 = in[7:0]; wire [7:0] b1 = in[15:8]; wire [7:0] b2 = in[23:16]; wire [7:0] b3 = in[31:24]; wire aligned = (in[1:0] == 2'b00); assign out = aligned ? {b1, b1, b2, b3} : {b0, b1, b2, b3}; endmodule"
        },
        {
            "bug": "the top byte is not moved; everything else is shifted"
            "module": "module top_module (input [31:0] in, output [31:32] out); assign out[31:24] = in[31:24]; assign out[23:16] = in[7:0]; assign out[15:8] = in[15:8]; assign out[7:0] = in[23:16]; endmodule"
        }
    ]
    </mutants>
</example>
"""

class MutantItem(BaseModel):
    bug: str
    module: str

class TBOutputFormat(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    reasoning: str
    mutants: List[MutantItem]

class MutantGenerator:
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

    def parse_output(self, response: ChatResponse) -> TBOutputFormat:
        try:
            output_json_obj: Dict = json.loads(response.message.content, strict=False)
            mutants = output_json_obj["mutants"]
            if isinstance(mutants, dict):
                mutants = [mutants]
            elif not isinstance(mutants, list):
                mutants = []

            ret = TBOutputFormat(
                reasoning=output_json_obj["reasoning"], 
                mutants=mutants
            )
        except json.decoder.JSONDecodeError:
            return TBOutputFormat(reasoning="", mutants=[])
        return ret

    def generate(self, messages: List[ChatMessage]) -> ChatResponse:
        logger.info(f" input message: {messages}")
        resp, token_cnt = self.token_counter.count_chat(messages)
        logger.info(f"Token count: {token_cnt}")
        logger.info(f"{resp.message.content}")
        return resp

    def run(
        self,
        mutants_path: str,
        golden_module: str,
    ) -> str:
        msg = [
            ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
            ChatMessage(
                content=GENERATION_PROMPT.format(
                    module=golden_module,
                    format=EXAMPLE_OUTPUT,
                    example=FEW_SHOT_EXAMPLE,
                ),
                role=MessageRole.USER,
            ),
            # ChatMessage(
            #     content=EXTRA_PROMPT,
            #     role=MessageRole.USER,
            # ),
        ]
        msg.append(
            ChatMessage(
                content=ORDER_PROMPT.format(
                    output_format="".join(json.dumps(EXAMPLE_OUTPUT, indent=4))
                ),
                role=MessageRole.USER,
            )
        )

        response = self.generate(msg)
        mutants_list = self.parse_output(response).mutants

        modules = ""

        for i, m in enumerate(mutants_list):
            output_path = os.path.join(mutants_path, f"top_{i+1}.v")
            mutant_str = ""
            mutant_str += f"// bug: {m.bug}\n\n"
            mutant_str += f"{m.module}\n"
            modules += mutant_str
            with open(output_path, "w") as f:
                f.write(mutant_str)

        logger.info(f"Get response from {self.model}: {response}")

        return modules  # Return string instead of list



