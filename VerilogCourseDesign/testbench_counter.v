`include "global_define.v"

module testbench_counter();

reg clk;
reg rst;
wire[15:0] time_data_bus;
wire[15:0] distance_data_bus;

time_counter instance_time_counter(
    .clk(clk),
    .rst(rst),
    .data(time_data_bus)
);

distance_counter instance_distance_counter(
    .clk(clk),
    .rst(rst),
    .data(distance_data_bus)
);

always begin
    #1;
    clk <= ~clk;
end

initial begin
    clk <= 1'b1;
    rst <= 1'b1;
    #5;
    rst <= 1'b0;
    #5;
    rst <= 1'b1;
end

endmodule