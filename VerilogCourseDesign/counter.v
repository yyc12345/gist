`include "global_define.v"

module counter 
# (
    parameter BIT_WIDTH = 4,
    parameter MAX_VALUE = 15
)
(
    input wire clk,
    input wire rst,
    output reg[BIT_WIDTH - 1:0] count,
    output wire cout
);

assign cout = count == MAX_VALUE ? 1'b1 : 1'b0;

always @(posedge clk, negedge rst) begin
    if (!rst) count <= 0;
    else begin
        if (count >= MAX_VALUE) count <= 0;
        else count <= count + 1;
    end
end

endmodule