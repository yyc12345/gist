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

parameter hide_dot = 8'b10000000,
        show_dot = 8'b00000000;
parameter bcd_blank = 7'b1111111;

always @(bcd_data, need_dot) begin
    case (bcd_data)
        4'h0: led_data <= bcd_0 | (need_dot ? show_dot : hide_dot);
        4'h1: led_data <= bcd_1 | (need_dot ? show_dot : hide_dot);
        4'h2: led_data <= bcd_2 | (need_dot ? show_dot : hide_dot);
        4'h3: led_data <= bcd_3 | (need_dot ? show_dot : hide_dot);
        4'h4: led_data <= bcd_4 | (need_dot ? show_dot : hide_dot);
        4'h5: led_data <= bcd_5 | (need_dot ? show_dot : hide_dot);
        4'h6: led_data <= bcd_6 | (need_dot ? show_dot : hide_dot);
        4'h7: led_data <= bcd_7 | (need_dot ? show_dot : hide_dot);
        4'h8: led_data <= bcd_8 | (need_dot ? show_dot : hide_dot);
        4'h9: led_data <= bcd_9 | (need_dot ? show_dot : hide_dot);
        4'ha: led_data <= bcd_a | (need_dot ? show_dot : hide_dot);
        4'hb: led_data <= bcd_b | (need_dot ? show_dot : hide_dot);
        4'hc: led_data <= bcd_c | (need_dot ? show_dot : hide_dot);
        4'hd: led_data <= bcd_d | (need_dot ? show_dot : hide_dot);
        4'he: led_data <= bcd_e | (need_dot ? show_dot : hide_dot);
        4'hf: led_data <= bcd_f | (need_dot ? show_dot : hide_dot);
        default: led_data <= bcd_blank | (need_dot ? show_dot : hide_dot);
    endcase
end

endmodule