module top_module (
  input [31:0] in,
  output [31:0] out
);

  // BUG: byte chunks are shifted by one bit before reassembly
  assign out = {
    {in[7:1],   1'b0},     // shifted right
    {in[15:9],  in[8]},    // rotated incorrectly
    {in[23:17], in[16]},   // rotated incorrectly
    {in[31:25], in[24]}    // rotated incorrectly
  };

endmodule
