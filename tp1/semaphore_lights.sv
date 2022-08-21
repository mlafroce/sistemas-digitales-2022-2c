`timescale 1ns/1ns
module semaphore_lights(clk, clk_seconds, rst, green1, yellow1, red1, green2, yellow2, red2);

parameter GREEN_SECS=30;
parameter YELLOW_SECS=3;


input clk, rst, clk_seconds;

output reg green1 = 0, yellow1 = 0, red1 = 0, green2 = 0, yellow2 = 0, red2 = 0;

reg [7:0] counter = 0;

always@(posedge clk)
begin
  if (clk_seconds == 1)
  begin
    counter <= counter + 1;
    if (counter >= YELLOW_SECS && counter < YELLOW_SECS + GREEN_SECS)
      begin
        yellow1 <= 0;
        yellow2 <= 0;
        green1 <= 1;
        green2 <= 0;
        red1 <= 0;
        red2 <= 1;
      end
    else if(counter >= YELLOW_SECS + GREEN_SECS && counter < 2 * YELLOW_SECS + GREEN_SECS)
      begin
        yellow1 <= 1;
        yellow2 <= 1;
        green1 <= 0;
        green2 <= 0;
        red1 <= 0;
        red2 <= 0;
      end
    else if (counter >= 2 * YELLOW_SECS + GREEN_SECS && counter < 2*(YELLOW_SECS + GREEN_SECS))
      begin
        yellow1 <= 0;
        yellow2 <= 0;
        green1 <= 0;
        green2 <= 1;
        red1 <= 1;
        red2 <= 0;
      end
    else begin
        yellow1 <= 1;
        yellow2 <= 1;
        green1 <= 0;
        green2 <= 0;
        red1 <= 0;
        red2 <= 0;
      end
  end
end

endmodule
