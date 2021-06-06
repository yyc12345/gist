`include "global_define.v"

module distance_counter(
    input wire clk,
    input wire rst,
    output wire[15:0] data
);

wire counter_out[2:0];

counter #(.MAX_VALUE(4'd9), .BIT_WIDTH(4)) bit0(
    .clk(clk),
    .rst(rst),
    .count(data[3:0]),
    .cout(counter_out[0])
);
counter #(.MAX_VALUE(4'd9), .BIT_WIDTH(4)) bit1(
    .clk(~counter_out[0]),
    .rst(rst),
    .count(data[7:4]),
    .cout(counter_out[1])
);

counter #(.MAX_VALUE(4'd9), .BIT_WIDTH(4)) bit2(
    .clk(~counter_out[1]),
    .rst(rst),
    .count(data[11:8]),
    .cout(counter_out[2])
);
counter #(.MAX_VALUE(4'd9), .BIT_WIDTH(4)) bit3(
    .clk(~counter_out[2]),
    .rst(rst),
    .count(data[15:12]),
    .cout()
);

endmodule