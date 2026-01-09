`timescale 1ns / 1ps

module xilinx_jtag_bridge #(
    parameter int unsigned JTAG_CHAIN = 2  // Must match OpenOCD "riscv use_bscan_tunnel 2"
)(
    input  wire  clk_i,       // System Clock (Optional in this logic, but good practice)
    input  wire  rst_ni,      // System Reset

    // Interface to Cheshire SoC
    output logic tck_o,       
    output logic tms_o,       
    output logic tdi_o,       
    input  logic tdo_i        
);

  // 1. Signals matching the Arty Example
  logic CAPTURE, DRCK, RESET, SEL, SHIFT, TCK, TDI, TMS, UPDATE, TDO;

  // 2. BSCANE2 Instantiation (Identical to Arty example)
  BSCANE2 #(
      .JTAG_CHAIN(JTAG_CHAIN) // USER2 (2)
  ) BSCANE2_inst (
      .CAPTURE(CAPTURE),
      .DRCK(DRCK),        // Gated Clock (Only toggles when we are active)
      .RESET(RESET),
      .RUNTEST(),
      .SEL(SEL),
      .SHIFT(SHIFT),
      .TCK(TCK),          // Free-running TCK
      .TDI(TDI),          // Data FROM OpenOCD
      .TMS(TMS),
      .UPDATE(UPDATE),
      .TDO(TDO)           // Data TO OpenOCD
  );

  // 3. Shift Register Logic
  // The Tunnel Protocol usually sends packets of ~6 bits.
  // We need a register to hold them.
  logic [5:0] shift_reg; 

  // TDO Logic: What we send back to OpenOCD
  // When OpenOCD reads, it gets the TDO from the Core
  assign TDO = tdo_i;

  // 4. The State Machine (Arty Style)
  always @(posedge DRCK) begin
    // If OpenOCD resets the chain
    if (RESET) begin
      shift_reg <= 6'b0;
    end
    
    // If OpenOCD is shifting data in
    if (SHIFT) begin
      // Shift TDI into the register (LSB first usually)
      shift_reg <= {TDI, shift_reg[5:1]};
    end
  end

  // 5. Output Assignment (The "Translation")
  // OpenOCD 'riscv use_bscan_tunnel' packs the signals into these bits:
  // Bit 0: TDI
  // Bit 1: TMS
  // Bit 2: TCK
  //
  // We map the shift register directly to the outputs.
  always_comb begin
      tdi_o = shift_reg[0];
      tms_o = shift_reg[1];
      tck_o = shift_reg[2]; // Software-controlled TCK!
  end

endmodule
