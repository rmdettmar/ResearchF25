module top_module (
  input [31:0] in,
  output [31:32] out
);

  // BUG: the top byte is not moved; everything else is shifted
  assign out[31:24] = in[31:24]; // wrong — should have been in[7:0]
  assign out[23:16] = in[7:0];
  assign out[15:8]  = in[15:8];
  assign out[7:0]   = in[23:16];

endmodule
