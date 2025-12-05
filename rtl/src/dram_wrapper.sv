// Copyright 2024 ETH Zurich and University of Bologna.
// Solderpad Hardware License, Version 0.51, see LICENSE for details.
// SPDX-License-Identifier: SHL-0.51
//
// Cyril Koenig <cykoenig@iis.ee.ethz.ch>
// Paul Scheffler <paulsc@iis.ee.ethz.ch>
//
// Resize AXI AW, IW, and DW before connecting to a Xilinx DRAM controller.

`include "cheshire/typedef.svh"
`include "common_cells/registers.svh"

module dram_wrapper #(
  parameter type axi_soc_aw_chan_t = logic,
  parameter type axi_soc_w_chan_t  = logic,
  parameter type axi_soc_b_chan_t  = logic,
  parameter type axi_soc_ar_chan_t = logic,
  parameter type axi_soc_r_chan_t  = logic,
  parameter type axi_soc_req_t     = logic,
  parameter type axi_soc_resp_t    = logic
) (
  input  logic  soc_resetn_i,
  input  logic  soc_clk_i,

  input  logic  clk100,
  input  logic  clk_ddr,
  input  logic  clk_ref,
  input  logic  clk_ddr_dqs,

  input  logic        uart_dram_write_we_i,
  input  logic [31:0] uart_dram_write_addr_i,
  input  logic [31:0] uart_dram_write_data_i,
  input  logic        uart_dram_write_rst_i,

  // PHY interfaces

  output        ddr3_ck_p,
  output        ddr3_ck_n,
  inout  [15:0] ddr3_dq,
  inout  [1:0]  ddr3_dqs_n,
  inout  [1:0]  ddr3_dqs_p,
  output [13:0] ddr3_addr,
  output [2:0]  ddr3_ba,
  output        ddr3_ras_n,
  output        ddr3_cas_n,
  output        ddr3_we_n,
  output        ddr3_reset_n,
  output        ddr3_cke,
  output        ddr3_cs_n,
  output [1:0]  ddr3_dm,
  output        ddr3_odt,
  // DRAM AXI interface
  input  axi_soc_req_t  soc_req_i,
  output axi_soc_resp_t soc_rsp_o
);

  //////////////////////////////////////
  //  Configurations and definitions  //
  //////////////////////////////////////

  typedef struct packed {
    bit     EnCdc;
    integer CdcLogDepth;
    integer IdWidth;
    integer AddrWidth;
    integer DataWidth;
    integer StrobeWidth;
    integer MaxUniqIds;
    integer MaxTxns;
  } dram_cfg_t;

  localparam dram_cfg_t cfg = '{
    EnCdc         : 0,    // 200 MHz AXI (cf. CCdcLogDepth)
    CdcLogDepth   : 5,
    IdWidth       : 4,    // Fixed
    AddrWidth     : 30,
    DataWidth     : 64,
    StrobeWidth   : 8,
    MaxUniqIds    : 4,    // TODO: suboptimal, but limited by CVA6/LLC
    MaxTxns       : 1    // TODO: suboptimal, but limited by CVA6/LLC
  };

  localparam SocDataWidth = $bits(soc_req_i.w.data);
  localparam SocIdWidth   = $bits(soc_req_i.ar.id);
  localparam SocUserWidth = $bits(soc_req_i.ar.user);
  localparam SocAddrWidth = $bits(soc_req_i.ar.addr);

  // Define type after data width and address resizer
  `AXI_TYPEDEF_ALL(axi_dw, logic[SocAddrWidth-1:0], logic[SocIdWidth-1:0],
                   logic[cfg.DataWidth-1:0], logic[cfg.StrobeWidth-1:0],
                   logic[SocUserWidth-1:0])

  // Define type after data & id width resizers
  `AXI_TYPEDEF_ALL(axi_dw_iw, logic[SocAddrWidth-1:0], logic[cfg.IdWidth-1:0],
                   logic[cfg.DataWidth-1:0], logic[cfg.StrobeWidth-1:0],
                   logic[SocUserWidth-1:0])

  // Clock on which is clocked the DRAM AXI
  logic dram_axi_clk;
  logic dram_rst_o;

  // Signals before resizing
  axi_soc_req_t  soc_dresizer_req;
  axi_soc_resp_t soc_dresizer_rsp;

  // Signals after data width resizing
  axi_dw_req_t  dresizer_iresizer_req;
  axi_dw_resp_t dresizer_iresizer_rsp;

  // Signals after id width resizing
  axi_dw_iw_req_t  iresizer_cdc_req, cdc_dram_req;
  axi_dw_iw_resp_t iresizer_cdc_rsp, cdc_dram_rsp;

  // Entry signals
  assign soc_dresizer_req = soc_req_i;
  assign soc_rsp_o = soc_dresizer_rsp;

  ////////////////////
  //  DW converter  //
  ////////////////////

  axi_dw_converter #(
    .AxiMaxReads          ( cfg.MaxTxns   ),
    .AxiSlvPortDataWidth  ( SocDataWidth  ),
    .AxiMstPortDataWidth  ( cfg.DataWidth ),
    .AxiAddrWidth         ( SocAddrWidth  ),
    .AxiIdWidth           ( SocIdWidth    ),
    // Common AW, AR, B
    .aw_chan_t            ( axi_soc_aw_chan_t ),
    .b_chan_t             ( axi_soc_b_chan_t  ),
    .ar_chan_t            ( axi_soc_ar_chan_t ),
    // Manager W, R
    .mst_w_chan_t         ( axi_dw_w_chan_t ),
    .mst_r_chan_t         ( axi_dw_r_chan_t ),
    .axi_mst_req_t        ( axi_dw_req_t    ),
    .axi_mst_resp_t       ( axi_dw_resp_t   ),
    // Subordinate W, R
    .slv_w_chan_t         ( axi_soc_w_chan_t ),
    .slv_r_chan_t         ( axi_soc_r_chan_t ),
    .axi_slv_req_t        ( axi_soc_req_t  ),
    .axi_slv_resp_t       ( axi_soc_resp_t )
  ) i_axi_dw_converter (
    .clk_i      ( soc_clk_i    ),
    .rst_ni     ( soc_resetn_i ),
    .slv_req_i  ( soc_dresizer_req ),
    .slv_resp_o ( soc_dresizer_rsp ),
    .mst_req_o  ( dresizer_iresizer_req ),
    .mst_resp_i ( dresizer_iresizer_rsp )
  );

  //////////////////
  //  ID resizer  //
  //////////////////

  // TODO: Implement simpler solutions
  axi_iw_converter #(
    .AxiAddrWidth           ( SocAddrWidth  ),
    .AxiDataWidth           ( cfg.DataWidth ),
    .AxiUserWidth           ( SocUserWidth  ),
    .AxiSlvPortIdWidth      ( SocIdWidth    ),
    .AxiSlvPortMaxUniqIds   ( cfg.MaxUniqIds ),
    .AxiSlvPortMaxTxnsPerId ( cfg.MaxTxns    ),
    .AxiSlvPortMaxTxns      ( cfg.MaxTxns    ),
    .AxiMstPortIdWidth      ( cfg.IdWidth    ),
    .AxiMstPortMaxUniqIds   ( cfg.MaxUniqIds ),
    .AxiMstPortMaxTxnsPerId ( cfg.MaxTxns    ),
    .slv_req_t              ( axi_dw_req_t     ),
    .slv_resp_t             ( axi_dw_resp_t    ),
    .mst_req_t              ( axi_dw_iw_req_t  ),
    .mst_resp_t             ( axi_dw_iw_resp_t )
  ) i_axi_iw_converter (
    .clk_i      ( soc_clk_i    ),
    .rst_ni     ( soc_resetn_i ),
    .slv_req_i  ( dresizer_iresizer_req ),
    .slv_resp_o ( dresizer_iresizer_rsp ),
    .mst_req_o  ( iresizer_cdc_req ),
    .mst_resp_i ( iresizer_cdc_rsp )
  );

  ////////////////////////
  //  Instiantiate CDC  //
  ////////////////////////

  if (cfg.EnCdc) begin : gen_cdc
    axi_cdc #(
      .aw_chan_t  ( axi_dw_iw_aw_chan_t),
      .w_chan_t   ( axi_dw_iw_w_chan_t),
      .b_chan_t   ( axi_dw_iw_b_chan_t),
      .ar_chan_t  ( axi_dw_iw_ar_chan_t),
      .r_chan_t   ( axi_dw_iw_r_chan_t),
      .axi_req_t  ( axi_dw_iw_req_t),
      .axi_resp_t ( axi_dw_iw_resp_t),
      .LogDepth   ( cfg.CdcLogDepth )
    ) i_axi_cdc_mig (
      .src_clk_i  ( soc_clk_i    ),
      .src_rst_ni ( soc_resetn_i ),
      .src_req_i  ( iresizer_cdc_req ),
      .src_resp_o ( iresizer_cdc_rsp ),
      .dst_clk_i  ( dram_axi_clk ),
      .dst_rst_ni ( ~dram_rst_o  ),
      .dst_req_o  ( cdc_dram_req ),
      .dst_resp_i ( cdc_dram_rsp )
    );
  end else begin : gen_no_cdc
    assign cdc_dram_req     = iresizer_cdc_req;
    assign iresizer_cdc_rsp = cdc_dram_rsp;
  end

  ////////////////////////////////
  //  Map User, Resize Address  //
  ////////////////////////////////

  assign cdc_dram_rsp.b.user = '0;
  assign cdc_dram_rsp.r.user = '0;

  logic [cfg.AddrWidth-1:0] cdc_dram_req_aw_addr;
  logic [cfg.AddrWidth-1:0] cdc_dram_req_ar_addr;

  assign cdc_dram_req_aw_addr = cdc_dram_req.aw.addr[cfg.AddrWidth-1:0];
  assign cdc_dram_req_ar_addr = cdc_dram_req.ar.addr[cfg.AddrWidth-1:0];

  assign dram_axi_clk = soc_clk_i;
  assign dram_rst_o   = ~soc_resetn_i;

  dram_controller_axi #(
    .AXI_ID_WIDTH  ( cfg.IdWidth ),
    .AXI_ADDR_WIDTH( cfg.AddrWidth ),
    .AXI_DATA_WIDTH( cfg.DataWidth )
  ) dram_controller (
    .clk_i(soc_clk_i),
    .rst_ni(soc_resetn_i),

    .s_axi_awvalid(cdc_dram_req.aw_valid),
    .s_axi_awready(cdc_dram_rsp.aw_ready),
    .s_axi_awaddr(cdc_dram_req_aw_addr),
    .s_axi_awid(cdc_dram_req.aw.id),
    .s_axi_awlen(cdc_dram_req.aw.len),
    .s_axi_awsize(cdc_dram_req.aw.size),
    .s_axi_awburst(cdc_dram_req.aw.burst),
    .s_axi_awprot(cdc_dram_req.aw.prot),

    .s_axi_wvalid(cdc_dram_req.w_valid),
    .s_axi_wready(cdc_dram_rsp.w_ready),
    .s_axi_wdata(cdc_dram_req.w.data),
    .s_axi_wstrb(cdc_dram_req.w.strb),
    .s_axi_wlast(cdc_dram_req.w.last),

    .s_axi_bvalid(cdc_dram_rsp.b_valid),
    .s_axi_bready(cdc_dram_req.b_ready),
    .s_axi_bid(cdc_dram_rsp.b.id),
    .s_axi_bresp(cdc_dram_rsp.b.resp),

    .s_axi_arvalid(cdc_dram_req.ar_valid),
    .s_axi_arready(cdc_dram_rsp.ar_ready),
    .s_axi_araddr(cdc_dram_req_ar_addr),
    .s_axi_arid(cdc_dram_req.ar.id),
    .s_axi_arlen(cdc_dram_req.ar.len),
    .s_axi_arsize(cdc_dram_req.ar.size),
    .s_axi_arburst(cdc_dram_req.ar.burst),
    .s_axi_arprot(cdc_dram_req.ar.prot),

    .s_axi_rvalid(cdc_dram_rsp.r_valid),
    .s_axi_rready(cdc_dram_req.r_ready),
    .s_axi_rid(cdc_dram_rsp.r.id),
    .s_axi_rdata(cdc_dram_rsp.r.data),
    .s_axi_rresp(cdc_dram_rsp.r.resp),
    .s_axi_rlast(cdc_dram_rsp.r.last),

    .ddr3_reset_n(ddr3_reset_n),
    .ddr3_cke(ddr3_cke),
    .ddr3_ck_p(ddr3_ck_p),
    .ddr3_ck_n(ddr3_ck_n),
    .ddr3_cs_n(ddr3_cs_n),
    .ddr3_ras_n(ddr3_ras_n),
    .ddr3_cas_n(ddr3_cas_n),
    .ddr3_we_n(ddr3_we_n),
    .ddr3_ba(ddr3_ba),
    .ddr3_addr(ddr3_addr),
    .ddr3_odt(ddr3_odt),
    .ddr3_dm(ddr3_dm),
    .ddr3_dqs_p(ddr3_dqs_p),
    .ddr3_dqs_n(ddr3_dqs_n),
    .ddr3_dq(ddr3_dq),

    .clk100(clk100),
    .clk_ddr(clk_ddr),
    .clk_ref(clk_ref),
    .clk_ddr_dqs(clk_ddr_dqs),

    .uart_dram_write_we_i(uart_dram_write_we_i),
    .uart_dram_write_addr_i(uart_dram_write_addr_i),
    .uart_dram_write_data_i(uart_dram_write_data_i),
    .uart_dram_write_rst_i(uart_dram_write_rst_i)
  );

endmodule
