`include "global_define.v"

module testbench_fare_adder();

reg clk_distance;
reg clk_time;
reg rst;
wire[15:0] data_bus;

fare_adder instance_fare_adder(
    .add_distance(clk_distance),
    .add_time(clk_time),
    .rst(rst),
    .data(data_bus)
);

initial begin
    clk_time <= 1'b0;
    clk_distance <= 1'b0;
    rst <= 1'b1;
    #5;
    rst <= 1'b0;
    #5;
    rst <= 1'b1;

    repeat(21) begin
        #1
        clk_time <= ~clk_time;
        #1
        clk_time <= ~clk_time;
    end

    #5;
    rst <= 1'b0;
    #5;
    rst <= 1'b1;

    repeat(2) begin
        #1
        clk_time <= ~clk_time;
        #1
        clk_time <= ~clk_time;
    end

    repeat(6) begin
        #1
        clk_distance <= ~clk_distance;
        #1
        clk_distance <= ~clk_distance;
    end

end

endmodule