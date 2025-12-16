module top_module (
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
