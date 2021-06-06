`include "global_define.v"

module testbench_taxi_fare();

reg clk;
reg[1:0] switch;
reg button_rst, button_distance, button_time;
wire[3:0] led_selector;
wire[7:0] led_data;

taxi_fare instance_taxi_fare(
    .clk(clk),
    .switch(switch),
    .button_rst(button_rst),
    .button_distance(button_distance),
    .button_time(button_time),
    .led_selector(led_selector),
    .led_data(led_data)
);

always begin
    #1;
    clk <= ~clk;
end

initial begin
    clk <= 1'b1;
    switch <= 2'b00;
    button_rst <= 1'b0;
    button_distance <= 1'b0;
    button_time <= 1'b0;

    #15;
    button_rst <= 1'b1;
    #7;
    button_rst <= 1'b0;

    /*
    #15;
    repeat(21) begin
        button_time <= 1'b1;
        #7;
        button_time <= 1'b0;
        #7;
    end
    */

    #15;
    repeat(6) begin
        button_distance <= 1'b1;
        #7;
        button_distance <= 1'b0;
        #7;
    end

    #15;
    switch <= 2'b01;
    #15;
    switch <= 2'b10;
    #15;
    switch <= 2'b11;

end

endmodule