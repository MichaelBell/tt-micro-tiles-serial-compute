/*
 * Shift register with ALU
 *
 * Copyright (C) 2024 Michael Bell
 */

`default_nettype none

module tt_um_MichaelBell_shift_compute (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  reg [15:0] shift_reg;
  reg [7:0] result_add;
  reg [7:0] result_and;

  always @(posedge clk) begin
    shift_reg <= {shift_reg[14:0], ui_in[0]};
    if (ui_in[4]) result_add <= shift_reg[15:8] + shift_reg[7:0];
    if (ui_in[5]) result_and <= shift_reg[15:8] & shift_reg[7:0];
  end

  reg [7:0] result;
  always @* begin
    case (ui_in[2:1])
      2'b00: result = shift_reg[7:0];
      2'b01: result = shift_reg[15:8];
      2'b10: result = result_add;
      2'b11: result = result_and;
      default: result = ui_in;
    endcase
  end

  assign uo_out = rst_n ? result : ui_in;

endmodule  // tt_um_MichaelBell_shift_compute
