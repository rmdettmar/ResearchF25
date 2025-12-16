module top_module (
  input [32:0] in,
  output [31:0] out
);

  // BUG: in[23:16] is duplicated, in[7:0] is never used
  assign out = {
    in[23:16],
    in[15:8],
    in[23:16],   // repeated
    in[31:24]
  };

endmodule
