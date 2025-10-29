`timescale 1ns/1ps

`include "cheshire/typedef.svh"

`define DRAM_SIM
`define SIM

module cheshire_soc_wrap import cheshire_pkg::*; #(
  parameter int unsigned SelectedCfg = 32'd0,
  parameter bit          UseDramSys  = 1'b0,
  parameter time          ClkPeriodRtc      = 30518ns,
  parameter int unsigned  RstCycles         = 5,
)
(
  input  logic clk_i,
  input  logic rst_ni,
  input  logic [1:0] boot_mode_i,

  // JTAG
  input  logic jtag_tck,
  input  logic jtag_trst_n,
  input  logic jtag_tms,
  input  logic jtag_tdi,
  output logic jtag_tdo,
  // UART
  output logic uart_tx,
  input  logic uart_rx,
  // I2C
  inout  logic i2c_sda,
  inout  logic i2c_scl,
  // SPI Host
  inout  logic                  spih_sck,
  inout  logic [SpihNumCs-1:0]  spih_csb,
  inout  logic [3:0]            spih_sd,
  // Serial Link
  input  logic [SlinkNumChan-1:0]                    slink_rcv_clk_i,
  output logic [SlinkNumChan-1:0]                    slink_rcv_clk_o,
  input  logic [SlinkNumChan-1:0][SlinkNumLanes-1:0]  slink_i,
  output logic [SlinkNumChan-1:0][SlinkNumLanes-1:0]  slink_o,

`ifndef DRAM_SIM
  // DDR3 Interface
  output logic ddr3_reset_n,
  output logic ddr3_cke,
  output logic ddr3_ck_p,
  output logic ddr3_ck_n,
  output logic ddr3_cs_n,
  output logic ddr3_ras_n,
  output logic ddr3_cas_n,
  output logic ddr3_we_n,
  output logic [2:0] ddr3_ba,
  output logic [13:0] ddr3_addr,
  output logic ddr3_odt,
  inout  logic [1:0] ddr3_dm,
  inout  logic [1:0] ddr3_dqs_p,
  inout  logic [1:0] ddr3_dqs_n,
  inout  logic [15:0] ddr3_dq
`endif
);

  logic test_mode = 0;
  
  logic rtc;
  `ifdef SIM
  clk_rst_gen #(
    .ClkPeriod    ( ClkPeriodRtc ),
    .RstClkCycles ( RstCycles )
  ) i_clk_rst_rtc (
    .clk_o  ( rtc ),
    .rst_no ( )
  );
  `else
  assign rtc = 1'b0;
  `endif

  import tb_cheshire_pkg::*;
  localparam cheshire_cfg_t WrapCfg = TbCheshireConfigs[SelectedCfg];
  `CHESHIRE_TYPEDEF_ALL(, WrapCfg)

  axi_llc_req_t axi_llc_mst_req;
  axi_llc_rsp_t axi_llc_mst_rsp;

  logic i2c_sda_o;
  logic i2c_sda_i;
  logic i2c_sda_en;
  logic i2c_scl_o;
  logic i2c_scl_i;
  logic i2c_scl_en;

  logic                 spih_sck_o;
  logic                 spih_sck_en;
  logic [SpihNumCs-1:0] spih_csb_o;
  logic [SpihNumCs-1:0] spih_csb_en;
  logic [3:0]           spih_sd_o;
  logic [3:0]           spih_sd_i;
  logic [3:0]           spih_sd_en;

  cheshire_soc #(
    .Cfg                ( WrapCfg ),
    .ExtHartinfo        ( '0 ),
    .axi_ext_llc_req_t  ( axi_llc_req_t ),
    .axi_ext_llc_rsp_t  ( axi_llc_rsp_t ),
    .axi_ext_mst_req_t  ( axi_mst_req_t ),
    .axi_ext_mst_rsp_t  ( axi_mst_rsp_t ),
    .axi_ext_slv_req_t  ( axi_slv_req_t ),
    .axi_ext_slv_rsp_t  ( axi_slv_rsp_t ),
    .reg_ext_req_t      ( reg_req_t ),
    .reg_ext_rsp_t      ( reg_rsp_t )
  ) csoc (
    .clk_i              ( clk       ),
    .rst_ni             ( rst_n     ),
    .test_mode_i        ( test_mode ),
    .boot_mode_i        ( boot_mode ),
    .rtc_i              ( rtc       ),
    .axi_llc_mst_req_o  ( axi_llc_mst_req ),
    .axi_llc_mst_rsp_i  ( axi_llc_mst_rsp ),
    .axi_ext_mst_req_i  ( '0 ),
    .axi_ext_mst_rsp_o  ( ),
    .axi_ext_slv_req_o  ( ),
    .axi_ext_slv_rsp_i  ( '0 ),
    .reg_ext_slv_req_o  ( ),
    .reg_ext_slv_rsp_i  ( '0 ),
    .intr_ext_i         ( '0 ),
    .intr_ext_o         ( ),
    .xeip_ext_o         ( ),
    .mtip_ext_o         ( ),
    .msip_ext_o         ( ),
    .dbg_active_o       ( ),
    .dbg_ext_req_o      ( ),
    .dbg_ext_unavail_i  ( '0 ),
    .jtag_tck_i         ( jtag_tck    ),
    .jtag_trst_ni       ( jtag_trst_n ),
    .jtag_tms_i         ( jtag_tms    ),
    .jtag_tdi_i         ( jtag_tdi    ),
    .jtag_tdo_o         ( jtag_tdo    ),
    .jtag_tdo_oe_o      ( ),
    .uart_tx_o          ( uart_tx ),
    .uart_rx_i          ( uart_rx ),
    .uart_rts_no        ( ),
    .uart_dtr_no        ( ),
    .uart_cts_ni        ( 1'b0 ),
    .uart_dsr_ni        ( 1'b0 ),
    .uart_dcd_ni        ( 1'b0 ),
    .uart_rin_ni        ( 1'b0 ),
    .i2c_sda_o          ( i2c_sda_o  ),
    .i2c_sda_i          ( i2c_sda_i  ),
    .i2c_sda_en_o       ( i2c_sda_en ),
    .i2c_scl_o          ( i2c_scl_o  ),
    .i2c_scl_i          ( i2c_scl_i  ),
    .i2c_scl_en_o       ( i2c_scl_en ),
    .spih_sck_o         ( spih_sck_o  ),
    .spih_sck_en_o      ( spih_sck_en ),
    .spih_csb_o         ( spih_csb_o  ),
    .spih_csb_en_o      ( spih_csb_en ),
    .spih_sd_o          ( spih_sd_o   ),
    .spih_sd_en_o       ( spih_sd_en  ),
    .spih_sd_i          ( spih_sd_i   ),
    .gpio_i             ( '0 ),
    .gpio_o             ( ),
    .gpio_en_o          ( ),
    .slink_rcv_clk_i    ( slink_rcv_clk_i ),
    .slink_rcv_clk_o    ( slink_rcv_clk_o ),
    .slink_i            ( slink_i ),
    .slink_o            ( slink_o ),
    .vga_hsync_o        ( ),
    .vga_vsync_o        ( ),
    .vga_red_o          ( ),
    .vga_green_o        ( ),
    .vga_blue_o         ( ),
    .usb_clk_i          ( 1'b0 ),
    .usb_rst_ni         ( 1'b1 ),
    .usb_dm_i           ( '0 ),
    .usb_dm_o           ( ),
    .usb_dm_oe_o        ( ),
    .usb_dp_i           ( '0 ),
    .usb_dp_o           ( ),
    .usb_dp_oe_o        ( )
  );

  assign i2c_sda = i2c_sda_en ? i2c_sda_o : 1'bz;
  assign i2c_sda_i = i2c_sda;
  assign i2c_scl = i2c_scl_en ? i2c_scl_o : 1'bz;
  assign i2c_scl_i = i2c_scl;

  assign spih_sck = spih_sck_en ? spih_sck_o : 1'bz;
  assign spih_csb = spih_csb_en;
  assign spih_sd  = spih_sd_en;
  assign spih_sd_i = spih_sd;

  `ifdef DRAM_SIM
    wire ddr3_reset_n;
    wire ddr3_cke;
    wire ddr3_ck_p;
    wire ddr3_ck_n;
    wire ddr3_cs_n;
    wire ddr3_ras_n;
    wire ddr3_cas_n;
    wire ddr3_we_n;
    wire [2:0] ddr3_ba;
    wire [13:0] ddr3_addr;
    wire ddr3_odt;
    wire [1:0] ddr3_dm;
    wire [1:0] ddr3_dqs_p;
    wire [1:0] ddr3_dqs_n;
    wire [15:0] ddr3_dq;

    ddr3 ddr3_dut (
      .rst_n  (ddr3_reset_n),
      .ck     (ddr3_ck_p),
      .ck_n   (ddr3_ck_n),
      .cke    (ddr3_cke),
      .cs_n   (ddr3_cs_n),
      .ras_n  (ddr3_ras_n),
      .cas_n  (ddr3_cas_n),
      .we_n   (ddr3_we_n),
      .dm_tdqs(ddr3_dm),
      .ba     (ddr3_ba),
      .addr   (ddr3_addr),
      .dq     (ddr3_dq),
      .dqs    (ddr3_dqs_p),
      .dqs_n  (ddr3_dqs_n),
      .tdqs_n (),
      .odt    (ddr3_odt)
    );
  `else
    
  `endif

endmodule
