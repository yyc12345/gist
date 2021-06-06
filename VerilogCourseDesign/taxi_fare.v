`include "global_define.v"

module taxi_fare(
    input wire clk,
    input wire[1:0] switch,
    input wire button_rst,
    input wire button_distance,
    input wire button_time,
    output wire[3:0] led_selector,
    output wire[7:0] led_data
);

reg[15:0] led_bcd_data_bus;
wire[15:0] debounce_data_bus;
wire[15:0] fare_data_bus;
wire[15:0] distance_data_bus;
wire[15:0] time_data_bus;
reg internal_rst, internal_add_distance, internal_add_time;

led_driver instance_led_driver(
    .input_data(led_bcd_data_bus),
    .clk(clk),
    .led_selector(led_selector),
    .led_data(led_data)
);
fare_adder instance_fare_adder(
    .add_distance(internal_add_distance),
    .add_time(internal_add_time),
    .rst(internal_rst),
    .data(fare_data_bus)
);
time_counter instance_time_counter(
    .clk(internal_add_time),
    .rst(internal_rst),
    .data(time_data_bus)
);
distance_counter instance_distance_counter(
    .clk(internal_add_time),
    .rst(internal_rst),
    .data(distance_data_bus)
);

debounce instance_debounce(
    .in_data(fare_data_bus),
    .out_data(debounce_data_bus)
);

always @(switch) begin
    case (switch)
        2'd0: assign led_bcd_data_bus = debounce_data_bus;
        2'd1: assign led_bcd_data_bus = distance_data_bus;
        2'd2: assign led_bcd_data_bus = time_data_bus;
        default: assign led_bcd_data_bus = 16'b0;
    endcase
end

always @(button_rst) begin
    internal_rst <= ~button_rst;
end
always @(button_distance) begin
    internal_add_distance <= button_distance;
end
always @(button_time) begin
    internal_add_time <= button_time;
end

endmodule