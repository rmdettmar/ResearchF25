import json
from typing import Dict

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from .mage.gen_config import get_llm
from .mage.log_utils import get_logger
from .mage.prompts import ORDER_PROMPT
from .mage.token_counter import TokenCounter, TokenCounterCached

logger = get_logger(__name__)

SYSTEM_PROMPT = r"""
You are an expert in RTL design. You can always write SystemVerilog code with no syntax errors and always reach correct functionality.
"""

GENERATION_PROMPT = r"""
You are given a specification (spec) intended for generating RTL code. Carefully read the provided spec and determine if it contains ambiguities. Specifically:

{circuit_type_prompt}

{example_prompt}
<input_spec>
{input_spec}
</input_spec>
"""
SEQUENTIAL_PROMPT = r"""
The logic described is sequential, ambiguities could include:

Timing/Clock Ambiguity (e.g., unclear clock edge or timing requirements)
Reset Conditions Ambiguity (unclear reset conditions or types)
State Transition Ambiguity (incomplete or unclear state transitions)
Clearly indicate your judgment by choosing one of the following options:
(a) No ambiguity, spec is clear and complete.
(b) Contains ambiguity type: [Timing/Clock]
(c) Contains ambiguity type: [Reset Conditions]
(d) Contains ambiguity type: [State Transition]
If ambiguity exists, provide exactly one short supplementary sentence per ambiguity to clarify the spec.

"""

CMB_PROMPT = r"""the logic described is combinational, ambiguities could include:
Incomplete Sensitivity Ambiguity (input sensitivity not fully defined)
Priority/Precedence Ambiguity (operation priority unclear)
Output Conditions Ambiguity (output not clearly defined for some inputs)
Clearly indicate your judgment by choosing one of the following options:
(a) No ambiguity, spec is clear and complete.
(b) Contains ambiguity type: [Incomplete Sensitivity]
(c) Contains ambiguity type: [Priority/Precedence]
(d) Contains ambiguity type: [Output Conditions]

"""
EXAMPLE_OUTPUT_FORMAT = {
    "reasoning": "All reasoning steps",
    "classification": "a/b/c/d(do not use any other words)",
    "clarification": {
        "ambiguity_1": "one concise clarification sentence",
        "ambiguity_2": "one concise clarification sentence",
    },
}
CLASSIFICATION_0_SHOT_EXAMPLES = r""" """
CLASSIFICATION_5_SHOT_EXAMPLES = r"""
Here are some examples of RTL ambiguity detection:
Example 1:
<example>
    "input_spec": "

// Specification:
// 1. The module shall process incoming data when enable=1
// 2. data_valid must be asserted when processing completes
// 3. Processing takes 1-3 cycles depending on data value
    ",
    "reasoning": r"
[Ambiguity 1]
    Source Clause: "Processing takes 1-3 cycles depending on data value"
    Type: Timing Unspecified
    Conflict Implementations:
        // Version A: Fixed 3-cycle pipeline
        always_ff @(posedge clk) begin
            if (data_in[31]) pipe_stage <= 3;
            else            pipe_stage <= 1;
        end

        // Version B: Variable latency
        always_comb begin
            case(data_in[31:30])
                2'b11: latency = 3;
                2'b01: latency = 2;
                default: latency = 1;
            endcase
        end

    Waveform Impact:
        Version A: Ignores 2-bit encoding, uses single-bit decision
        Version B: Fully utilizes 2-bit control field

    Clarification: "Processing latency shall be determined by bits[31:30] as:
                   2'b11:3 cycles, 2'b01:2 cycles, others:1 cycle"

    SVA Assertion:
        assert property (@(posedge clk) disable iff (!rst_n)
            (enable && data_in[31:30]==2'b11) |-> \#\#3 data_valid);
        assert property (@(posedge clk) disable iff (!rst_n)
            (enable && data_in[31:30]==2'b01) |-> \#\#2 data_valid);
        assert property (@(posedge clk) disable iff (!rst_n)
            (enable && data_in[31:30]!=2'b11 && data_in[31:30]!=2'b01) |-> \#\#1 data_valid);

",
    "classification": "ambiguous"
</example>

Example 2:
<example>
    "input_spec": "
// Module: arbiter
// Requirements:
// - Supports 4 requestors with priority 0(highest)-3(lowest)
// - grant signal must be asserted within 2 cycles after req
// - Preemption allowed for higher priority requests
    ",
    "reasoning": r"
[Ambiguity 1]
    Source Clause: "Preemption allowed for higher priority requests"
    Type: State Machine Overlap
    Conflict Implementations:
        // Version A: Immediate preemption
        always_comb begin
            grant = 4'b0;
            priority casez(req)
                4'b???1: grant = 4'b0001;
                4'b??10: grant = 4'b0010;
                4'b?100: grant = 4'b0100;
                4'b1000: grant = 4'b1000;
            endcase
        end

        // Version B: Cycle-boundary preemption
        always_ff @(posedge clk) begin
            if(current_grant && higher_priority_req)
                grant <= 1 << get_highest_priority(req);
        end

    Waveform Impact:
        Version A: Mid-cycle grant changes
        Version B: Grants update only at clock edges

    Clarification: "Preemption shall only occur at clock boundaries"

    SVA Assertion:
        assert property (@(posedge clk)
            $changed(grant) |-> !$isunknown(clk));
",
    "classification": "ambiguous"
</example>

Example 3:
<example>
    "input_spec": "
// Module: serial_parser
// Functionality:
// - Start parsing when start_pulse=1
// - Detect sync pattern 0xA5 in first 2 bytes
// - Assert error_flag if invalid header within 16 cycles
// - All operations synchronous to clk (100MHz)
    ",
[Ambiguity 1]
    Source Clause: "Detect sync pattern 0xA5 in first 2 bytes"
    Type: Boundary Condition Gap
    Conflict Implementations:
        // Version A: Check first 16 bits
        assign sync_ok = (data_stream[15:0] == 16'hA5);

        // Version B: Check any consecutive 8 bits
        always_comb begin
            sync_ok = 0;
            for(int i=0; i<16; i++)
                if(data_stream[i+:8] == 8'hA5)
                    sync_ok = 1;
        end

    Waveform Impact:
        Version A: Detects sync only at bits[15:0]
        Version B: May detect sync at bits[7:0], [8:1], ..., [23:16]

    Clarification: "Sync pattern must match the first two bytes exactly"

    SVA Assertion:
        assert property (@(posedge clk)
            start_pulse |-> \#\#0 data_stream[15:0]==16'hA5);
",
    "classification": "ambiguous"
</example>

"""

EXTRA_ORDER_PROMPT = r"""
VERY IMPORTANT: Please only include "reasoning" and "classification" in your response.
Do not include any other information in your response, like 'json', 'example', 'Let me analyze','input_spec' or '<output_format>'.
Key instruction: Direct output, no extra comments.
As a reminder, please directly provide the content without adding any extra comments or explanations.
"""


class ambiguous_classifier:
    def __init__(
        self,
        model: str,
        max_token: int,
        provider: str,
        cfg_path: str,
        top_p: float,
        temperature: float,
    ):
        self.model = model
        self.llm = get_llm(
            model=model,
            max_token=max_token,
            provider=provider,
            cfg_path=cfg_path,
            top_p=top_p,
            temperature=temperature,
        )
        self.token_counter = (
            TokenCounterCached(self.llm)
            if TokenCounterCached.is_cache_enabled(self.llm)
            else TokenCounter(self.llm)
        )

    def run(self, input_spec: str, circuit_type: str) -> Dict:
        if isinstance(self.token_counter, TokenCounterCached):
            self.token_counter.set_enable_cache(True)
        self.token_counter.reset()
        self.token_counter.set_cur_tag(self.__class__.__name__)
        if circuit_type == "SEQ":
            msg = [
                ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
                ChatMessage(
                    content=GENERATION_PROMPT.format(
                        input_spec=input_spec,
                        circuit_type_prompt=SEQUENTIAL_PROMPT,
                        example_prompt=CLASSIFICATION_0_SHOT_EXAMPLES,
                    ),
                    role=MessageRole.USER,
                ),
                ChatMessage(
                    content=ORDER_PROMPT.format(
                        output_format="".join(
                            json.dumps(EXAMPLE_OUTPUT_FORMAT, indent=4)
                        )
                    ),
                    role=MessageRole.USER,
                ),
            ]
        elif circuit_type == "CMB":
            msg = [
                ChatMessage(content=SYSTEM_PROMPT, role=MessageRole.SYSTEM),
                ChatMessage(
                    content=GENERATION_PROMPT.format(
                        input_spec=input_spec,
                        circuit_type_prompt=SEQUENTIAL_PROMPT,
                        example_prompt=CLASSIFICATION_0_SHOT_EXAMPLES,
                    ),
                    role=MessageRole.USER,
                ),
                ChatMessage(
                    content=ORDER_PROMPT.format(
                        output_format="".join(
                            json.dumps(EXAMPLE_OUTPUT_FORMAT, indent=4)
                        )
                    ),
                    role=MessageRole.USER,
                ),
            ]
        response, token_cnt = self.token_counter.count_chat(msg)

        logger.info(f"Token count: {token_cnt}")
        logger.info(f"{response.message.content}")
        self.token_counter.log_token_stats()

        # response = self.generate(msg)
        logger.info(f"Get response from {self.model}: {response.message.content}")
        try:
            # output_json_obj: Dict = json.loads(response.message.content, strict=False)

            # use this for Deepseek r1 and claude-3-5-sonnet
            # if self.model == "claude-3-5-sonnet-20241022":
            #     output_json_obj: Dict = json.loads("".join(response.choices[0].message.content.split("\n")[1:]), strict=False)
            # else:
            #     output_json_obj: Dict = json.loads(response.choices[0].message.content, strict=False)
            output_json_obj: Dict = json.loads(response.message.content, strict=False)

            classification = output_json_obj["classification"]
            logger.info(f"Succeed to parse response, Classification: {classification}")
        except json.decoder.JSONDecodeError as e:
            print(f"Json parse error: {e}")
            logger.info(f"Json parse error: {e}")
            print(response)
            return None

        return output_json_obj
