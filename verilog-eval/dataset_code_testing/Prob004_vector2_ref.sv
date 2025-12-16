module RefModule (
  input [31:0] in,
  output [31:0] out
);

  assign out = {in[7:0], in[15:8], in[23:16], in[31:24]};

endmodule

/* verilator lint_off MULTITOP */

module TestModuleI (
  input [31:0] in,
  output [31:32] out
);

  // BUG: the top byte is not moved; everything else is shifted
  assign out[31:24] = in[31:24]; // wrong — should have been in[7:0]
  assign out[23:16] = in[7:0];
  assign out[15:8]  = in[15:8];
  assign out[7:0]   = in[23:16];

endmodule

module TestModuleII (
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

module TestModuleIII (
  input [31:0] in,
  output [31:32] out
);

  // BUG: out[31:24] incorrectly uses in[15:8]
  assign out[31:24] = in[15:8];
  assign out[23:16] = in[7:0];
  assign out[15:8]  = in[23:16];
  assign out[7:0]   = in[31:24];

endmodule

module TestModuleIV (
  input [31:0] in,
  output [31:0] out
);

  // BUG: lower two bytes masked with zeros
  assign out = {
    in[7:0],
    in[15:8] & 8'hF0,   // masked high
    in[23:16] & 8'h0F,  // masked low
    in[31:24]
  };

endmodule

module TestModuleV (
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

module TestModule (
  input [31:0] in,
  output [31:0] out
);

  wire [7:0] b0 = in[7:0];
  wire [7:0] b1 = in[15:8];
  wire [7:0] b2 = in[23:16];
  wire [7:0] b3 = in[31:24];

  // Detect 4-byte alignment: lowest 2 bits are 0
  wire aligned = (in[1:0] == 2'b00);

  // BUG: for aligned inputs, top byte is wrong (uses b1 instead of b0)
  assign out = aligned
               ? {b1, b1, b2, b3}  // subtle aligned-case corruption
               : {b0, b1, b2, b3}; // correct behavior normally

endmodule
