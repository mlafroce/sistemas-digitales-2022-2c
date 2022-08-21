`timescale 1ns/1ns
module clock_divisor(clk, rst, clk_out);
  parameter DIVISOR=4;

  input clk, rst;

  output reg clk_out = 0;

  reg [8:0] counter = DIVISOR-1;

  always@(posedge clk)
  begin
    counter <= counter - 1;
    clk_out <= counter == 0 ? 1 : 0;
    if(counter == 0)
        counter <= DIVISOR-1;
  end
endmodule
