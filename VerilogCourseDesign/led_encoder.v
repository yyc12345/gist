`include "global_define.v"

module led_encoder(
    input wire[3:0] bcd_data,
    input wire need_dot,
    output reg[7:0] led_data    // follow abcdefgp, a is the lowest bit.
);

// led have the same anode, 1 is hide and 0 is show
parameter bcd_0 = 7'hc0,
        bcd_1 = 7'hf9,
        bcd_2 = 7'ha4,
        bcd_3 = 7'hb0,
        bcd_4 = 7'h99,
        bcd_5 = 7'h92,
        bcd_6 = 7'h82,
        bcd_7 = 7'hf8,
        bcd_8 = 7'h80,
        bcd_9 = 7'h90,
        bcd_a = 7'h88,
        bcd_b = 7'h83,
        bcd_c = 7'hc6,
        bcd_d = 7'ha1,
        bcd_e = 7'h86,
        bcd_f = 7'h8e;

parameter bcd_blank = 7'b1111111;

always @(bcd_data) begin
    case (bcd_data)
        4'h0: led_data[6:0] <= bcd_0;
        4'h1: led_data[6:0] <= bcd_1;
        4'h2: led_data[6:0] <= bcd_2;
        4'h3: led_data[6:0] <= bcd_3;
        4'h4: led_data[6:0] <= bcd_4;
        4'h5: led_data[6:0] <= bcd_5;
        4'h6: led_data[6:0] <= bcd_6;
        4'h7: led_data[6:0] <= bcd_7;
        4'h8: led_data[6:0] <= bcd_8;
        4'h9: led_data[6:0] <= bcd_9;
        4'ha: led_data[6:0] <= bcd_a;
        4'hb: led_data[6:0] <= bcd_b;
        4'hc: led_data[6:0] <= bcd_c;
        4'hd: led_data[6:0] <= bcd_d;
        4'he: led_data[6:0] <= bcd_e;
        4'hf: led_data[6:0] <= bcd_f;
        default: led_data[6:0] <= bcd_blank;
    endcase
end

always @(need_dot) begin
    led_data[7] <= ~need_dot;
end

endmodule