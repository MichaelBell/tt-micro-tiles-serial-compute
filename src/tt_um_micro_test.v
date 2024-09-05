/*
 * tt_um_factory_test.v
 *
 * Test user module
 *
 * Author: Sylvain Munaut <tnt@246tNt.com>
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
    case (ui_in[3:1])
      3'b001: result = shift_reg[7:0];
      3'b010: result = shift_reg[15:8];
      3'b100: result = result_add;
      3'b101: result = result_and;
      default: result = ui_in;
    endcase
  end

  assign uo_out = result;

endmodule  // tt_um_MichaelBell_shift_compute
