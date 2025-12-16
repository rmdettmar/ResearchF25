// bug: Output incorrectly depends on only two inputs

module top_module (input a, input b, input c, output out); assign out = (a | b); endmodule
