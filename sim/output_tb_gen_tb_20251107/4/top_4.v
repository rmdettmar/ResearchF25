module top_module (
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
