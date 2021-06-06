`include "global_define.v"

module debounce(
    input wire[15:0] in_data,
    output reg[15:0] out_data
);

reg carry_bit1, carry_bit2;

always @(in_data[3:0]) begin
    if (in_data[15:4] < 12'd8) out_data[3:0] <= 4'd0;
    else out_data[3:0] <= in_data[3:0];
end

always @(in_data[7:4]) begin
    if (in_data[15:4] < 12'd8) out_data[7:4] <= 4'd8;
    else begin
        if (in_data[7:4] < 4'd8) begin
            carry_bit1 <= 1'b1;
            out_data[7:4] <= 4'd8 - in_data[7:4];
        end
        else begin
            carry_bit1 <= 1'b0;
            out_data[7:4] <= in_data[7:4] - 4'd8;
        end        
    end
end

always @(in_data[11:8], carry_bit1) begin
    if (in_data[15:4] < 12'd8) out_data[11:8] <= 4'd0;
    else begin
        if (!in_data[11:8] && carry_bit1) begin
            carry_bit2 <= 1'b1;
            out_data[11:8] <= in_data[11:8] - 4'd1;
        end
        else begin
            carry_bit2 <= 1'b1;
            out_data[11:8] <= in_data[11:8];
        end        
    end
end

always @(in_data[15:12], carry_bit2) begin
    if (in_data[15:4] < 12'd8) out_data[15:12] <= 4'd0;
    else begin
        if (!in_data[15:12] && carry_bit2) begin
            out_data[15:12] <= in_data[15:12] - 4'd1;
        end
        else begin
            out_data[15:12] <= in_data[15:12];
        end        
    end
end

endmodule