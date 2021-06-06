`include "global_define.v"

module simple_bcd_adder(
    input wire[3:0] a,
    input wire b,
    output reg[3:0] sum,
    output reg cou
);

always @(a, b) begin
    if (a == 4'd9 && b) begin
        cou <= 1'b1;
        sum <= 3'b0;
    end
    else begin
        cou <= 1'b0;
        sum <= a + {2'd0, b};
    end
end

endmodule