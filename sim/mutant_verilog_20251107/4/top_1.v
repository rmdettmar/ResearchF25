// bug: The second byte is swapped with the last byte, disrupting the intended order.

module top_module (input [31:0] in, output [31:0] out); assign out = {in[7:0], in[31:24], in[23:16], in[15:8]}; endmodule
