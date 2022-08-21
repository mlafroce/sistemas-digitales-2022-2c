`timescale 1ns/1ns
module counter(clk, enabled, reset, count);
    parameter N=8;

    input clk, enabled, reset;

    output reg [N:0] count = 0;

    always@(posedge clk)
    begin
        if(reset)
            count <= 0;
        else if (enabled)
            count <= count + 1;
    end

endmodule
