`timescale 1ns/1ns
module semaphore(clk, rst, green1, yellow1, red1, green2, yellow2, red2, dbg_seconds);
  input clk, rst;

  output dbg_seconds;
  output green1, yellow1, red1, green2, yellow2, red2;

  wire clk_seconds;
  assign dbg_seconds = clk_seconds;

  clock_divisor divisor ( .clk(clk), .rst(rst), .clk_out(clk_seconds));
  semaphore_lights lights (
    .clk(clk),
    .rst(rst),
    .clk_seconds(clk_seconds),
    .green1(green1),
    .yellow1(yellow1),
    .red1(red1),
    .green2(green2),
    .yellow2(yellow2),
    .red2(red2)
  );
  initial begin
    $dumpfile ("semaphore.vcd");
    $dumpvars (0, lights);
    #1;
  end
endmodule
