// bug: The second byte is skipped, and the first byte is duplicated.

module top_module (input [31:0] in, output [31:0] out); assign out = {in[7:0], in[7:0], in[23:16], in[31:24]}; endmodule
