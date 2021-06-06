`include "global_define.v"

module bcd_adder(
    input wire[3:0] a,
    input wire[3:0] b,
    output reg[3:0] sum,
    output reg cou
);

always @(a, b) begin
    if (a + b > 9) begin
        cou <= 1'b1;
        sum <= (a + b - 4'd10);
    end
    else begin
        cou <= 1'b0;
        sum <= a + b;
    end
end

endmodule