`include "global_define.v"

module fare_adder_core(
    input wire add_distance,
    input wire add_time,
    input wire rst,
    output wire[15:0] out_data
);

reg[15:0] input_cache;
reg[3:0] add_num;
wire counter_out[2:0];

bcd_adder bit0(
    .a(input_cache[3:0]),
    .b(add_num[3:0]),
    .sum(out_data[3:0]),
    .cou(counter_out[0])
);
simple_bcd_adder bit1(
    .a(input_cache[7:4]),
    .b(counter_out[0]),
    .sum(out_data[7:4]),
    .cou(counter_out[1])
);
simple_bcd_adder bit2(
    .a(input_cache[11:8]),
    .b(counter_out[1]),
    .sum(out_data[11:8]),
    .cou(counter_out[2])
);
simple_bcd_adder bit3(
    .a(input_cache[15:12]),
    .b(counter_out[2]),
    .sum(out_data[15:12]),
    .cou()
);

always @(negedge rst) begin
    input_cache <= 16'b1000_0000;
    add_num <= 4'd0;
end

always @(posedge add_distance) begin
    input_cache <= out_data;
    add_num <= 4'd8;
end

always @(posedge add_time) begin
    input_cache <= out_data;
    add_num <= 4'd4;
end

endmodule