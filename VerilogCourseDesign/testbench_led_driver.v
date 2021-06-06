`include "global_define.v"

module testbench_led_driver();

reg clk;
reg[15:0] input_data;
wire[3:0] output_selector;
wire[7:0] output_data;
reg time_display, fare_display;

led_driver instance_led_driver(
    .input_data(input_data),
    .clk(clk),
    .is_time_display(time_display),
    .is_fare_display(fare_display),
    .led_selector(output_selector),
    .led_data(output_data)
);

always begin
    #1;
    clk <= ~clk;
end

initial begin
    clk <= 1'b1;
    time_display <= 1'b0;
    fare_display <= 1'b0;
    #4;

    input_data <= 16'b0101_0110_0111_1110;
    #8;

    input_data <= 16'd0 << 4;
    #8;
    input_data <= 16'd1 << 4;
    #8;
    input_data <= 16'd2 << 4;
    #8;
    input_data <= 16'd3 << 4;
    #8;
    input_data <= 16'd4 << 4;
    #8;
    input_data <= 16'd5 << 4;
    #8;
    input_data <= 16'd6 << 4;
    #8;
    input_data <= 16'd7 << 4;
    #8;
    input_data <= 16'd8 << 4;
    #8;
    input_data <= 16'd9 << 4;
    #8;
    input_data <= 16'd10 << 4;
    #8;
    input_data <= 16'd11 << 4;
    #8;
    input_data <= 16'd12 << 4;
    #8;
    input_data <= 16'd13 << 4;
    #8;
    input_data <= 16'd14 << 4;
    #8;
    input_data <= 16'd15 << 4;
    #8;

    fare_display <= 1'b1;

    input_data <= 16'd0 << 4;
    #8;
    input_data <= 16'd1 << 4;
    #8;
    input_data <= 16'd2 << 4;
    #8;
    input_data <= 16'd3 << 4;
    #8;
    input_data <= 16'd4 << 4;
    #8;
    input_data <= 16'd5 << 4;
    #8;
    input_data <= 16'd6 << 4;
    #8;
    input_data <= 16'd7 << 4;
    #8;
    input_data <= 16'd8 << 4;
    #8;
    input_data <= 16'd9 << 4;
    #8;
    input_data <= 16'd10 << 4;
    #8;
    input_data <= 16'd11 << 4;
    #8;
    input_data <= 16'd12 << 4;
    #8;
    input_data <= 16'd13 << 4;
    #8;
    input_data <= 16'd14 << 4;
    #8;
    input_data <= 16'd15 << 4;
    #8;
end

endmodule