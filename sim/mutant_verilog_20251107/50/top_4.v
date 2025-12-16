// bug: Incorrectly uses AND instead of OR for one operand

module top_module (input a, input b, input c, output out); assign out = (a & b | c); endmodule
