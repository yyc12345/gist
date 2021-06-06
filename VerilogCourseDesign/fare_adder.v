`include "global_define.v"

module fare_adder(
    input wire add_distance,
    input wire add_time,
    input wire rst,
    output wire[15:0] data
);

wire add_distance_debounce, add_time_within_distance;
reg[4:0] time_trigger_count; // from 0 to 20, if this >= 21, keep it as 21 and add fare to 2 fare_adder at the same time, otherwise, only add for fare_adder instance.
reg[2:0] distance_trigger_count; // from 0 to 5, if this >= 6, keep it as 5 and assign data output.
wire[15:0] fare_data_bus;
wire[15:0] fare_within_distance_data_bus;

assign add_distance_debounce = distance_trigger_count >= 6 ? add_distance : 1'b0;
assign add_time_within_distance = time_trigger_count >= 21 ? add_time : 1'b0;
assign data = distance_trigger_count >= 6 ? fare_data_bus : fare_within_distance_data_bus;

// the fare out of 2.5 km
fare_adder_core fare_adder(
    .add_distance(add_distance_debounce),
    .add_time(add_time),
    .rst(rst),
    .out_data(fare_data_bus)
);

// the fare within 2.5 km
fare_adder_core fare_adder_within_distance(
    .add_distance(add_distance_debounce),
    .add_time(add_time_within_distance),
    .rst(rst),
    .out_data(fare_within_distance_data_bus)
);

always @(negedge rst) begin
    time_trigger_count <= 5'd0;
    distance_trigger_count <= 3'd0;
end

always @(posedge add_distance) begin
    if (distance_trigger_count >= 6) begin
        distance_trigger_count <= distance_trigger_count;
    end
    else begin
        distance_trigger_count <= distance_trigger_count + 3'd1;
    end
end

always @(posedge add_time) begin
    if (time_trigger_count >= 21) begin
        time_trigger_count <= time_trigger_count;
    end
    else begin
        time_trigger_count <= time_trigger_count + 5'd1;
    end
end

endmodule