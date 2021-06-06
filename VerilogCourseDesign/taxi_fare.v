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

parameter MODE_FARE = 2'd0,
        MODE_DISTANCE = 2'd1,
        MODE_TIME = 2'd2;

reg[15:0] led_bcd_data_bus;
wire[15:0] fare_data_bus;
wire[15:0] distance_data_bus;
wire[15:0] time_data_bus;
wire internal_rst, internal_add_distance, internal_add_time;
wire is_time_display, is_fare_display;

assign internal_rst = ~button_rst;
assign internal_add_distance = button_distance;
assign internal_add_time = button_time;
assign is_time_display = switch == MODE_TIME ? 1'b1 : 1'b0;
assign is_fare_display = switch == MODE_FARE ? 1'b1 : 1'b0;

led_driver instance_led_driver(
    .input_data(led_bcd_data_bus),
    .clk(clk),
    .is_time_display(is_time_display),
    .is_fare_display(is_fare_display),
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
    .clk(internal_add_distance),
    .rst(internal_rst),
    .data(distance_data_bus)
);

always @(switch) begin
    case (switch)
        MODE_FARE: assign led_bcd_data_bus = fare_data_bus;
        MODE_DISTANCE: assign led_bcd_data_bus = distance_data_bus;
        MODE_TIME: assign led_bcd_data_bus = time_data_bus;
        default: assign led_bcd_data_bus = 16'b0;
    endcase
end

endmodule