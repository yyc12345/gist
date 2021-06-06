`include "global_define.v"

module led_driver(
    input wire[15:0] input_data,
    input wire clk,
    input wire is_time_display,
    input wire is_fare_display,
    output reg[3:0] led_selector,   // led 0 enable signal is the lowest bit
    output wire[7:0] led_data
);

parameter enable_led0 = 4'b0001,
        enable_led1 = 4'b0010,
        enable_led2 = 4'b0100,
        enable_led3 = 4'b1000;

wire freq_splitter_out;
reg[3:0] gotten_bcd;
wire need_dot;

assign need_dot = ((led_selector == enable_led1) && is_fare_display) ? 1'b1 : 1'b0;

led_encoder led_coder(
    .bcd_data(gotten_bcd),
    .need_dot(need_dot),
    .led_data(led_data)
);

// instance a counter to reduce frequency
counter #(.MAX_VALUE(1023), .BIT_WIDTH(10)) freq_splitter(
    .clk(clk),
    .rst(1'b1),
    .count(),
    .cout(freq_splitter_out)
);

always @(posedge clk) begin
//always @(posedge freq_splitter_out) begin
    case (led_selector)
        enable_led0: begin
            led_selector <= enable_led1;
            gotten_bcd <= input_data[7:4];
        end
        enable_led1: begin
            led_selector <= enable_led2;
            gotten_bcd <= input_data[11:8];
        end
        enable_led2: begin
            led_selector <= enable_led3;
            gotten_bcd <= input_data[15:12];
        end
        enable_led3: begin
            led_selector <= enable_led0;
            gotten_bcd <= input_data[3:0];
        end
        default: begin
            led_selector <= enable_led0;
            gotten_bcd <= input_data[3:0];
        end
    endcase
end

endmodule