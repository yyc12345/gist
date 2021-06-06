`include "global_define.v"

module led_driver(
    input wire[15:0] input_data,
    input wire clk,
    input wire is_time_display,
    input wire is_fare_display,
    output reg[3:0] led_selector,   // led 0 enable signal is the lowest bit
    output wire[7:0] led_data
);

parameter enable_led0 = 4'b1110,
        enable_led1 = 4'b1101,
        enable_led2 = 4'b1011,
        enable_led3 = 4'b0111;

wire freq_splitter_out;
reg[3:0] gotten_bcd;
wire freq_splitter_out[1:0];
wire need_dot;

assign need_dot = ((led_selector == enable_led1) && is_fare_display) ? 1'b1 : 1'b0;

led_encoder led_coder(
    .bcd_data(gotten_bcd),
    .need_dot(need_dot),
    .led_data(led_data)
);

// instance a counter to reduce frequency
// this FPGA use 50MHz clock
// 2 freq splitter(1024 + 128) will reduce the freq to around 381Hz
// the best freq for 4 bit led displaying is 1KHz - 60Hz accoring to manual
// then minus 2 bit for the last splitter(128 -> 32), because led have 4 bit
// the splitted freq is used for the display duration for each bit, not 4 bits.
counter #(.MAX_VALUE(10'd1023), .BIT_WIDTH(10)) freq_splitter0(
    .clk(clk),
    .rst(1'b1),
    .count(),
    .cout(freq_splitter_out[0])
);
counter #(.MAX_VALUE(5'd31), .BIT_WIDTH(5)) freq_splitter1(
    .clk(~freq_splitter_out[0]),
    .rst(1'b1),
    .count(),
    .cout(freq_splitter_out[1])
);

always @(posedge clk) begin
//always @(negedge freq_splitter_out[1]) begin
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