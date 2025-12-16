// bug: Output incorrectly driven by constant 1'b0 if c is high

module top_module (input a, input b, input c, output out); assign out = (a | b | (c ? 1'b0 : c)); endmodule
