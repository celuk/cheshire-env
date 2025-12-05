import argparse
import os
import glob
from pathlib import Path

from cocotb.runner import get_runner

VIVADO_PATH = "/tools/Xilinx/Vivado/2022.2"
#VIVADO_PATH = "/home/kasirga/work/xilinx/tools/Xilinx/Vivado/2022.2"

ROOT="../../cheshire"

BINARY="../../../cheshire/sw/tests/helloworld.spm.elf"
BOOTMODE=0
PRELMODE=1

SCRIPT_DIR = Path(os.path.realpath(__file__)).parent.absolute()

DRAM_SIM = 1

FILE_LIST = [
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_verif_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/clk_rst_gen.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_id_queue.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_stream_mst.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_synch_holdable_driver.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/signal_highlighter.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/sim_timeout.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/stream_watchdog.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_synch_driver.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/src/rand_stream_slv.sv",
    f"{ROOT}/.bender/git/checkouts/common_verification-*/test/tb_clk_rst_gen.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/rtl/tc_sram.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/rtl/tc_sram_impl.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/rtl/tc_clk.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/cluster_pwr_cells.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/generic_memory.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/generic_rom.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/pad_functional.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/pulp_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/pulp_pwr_cells.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/tc_pwr.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/test/tb_tc_sram.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/pulp_clock_gating_async.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/cluster_clk_cells.sv",
    f"{ROOT}/.bender/git/checkouts/tech_cells_generic-*/src/deprecated/pulp_clk_cells.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/binary_to_gray.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cb_filter_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cc_onehot.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_reset_ctrlr_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cf_math_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/clk_int_div.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/credit_counter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/delta_counter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/ecc_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/edge_propagator_tx.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/exp_backoff.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/fifo_v3.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/gray_to_binary.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/isochronous_4phase_handshake.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/isochronous_spill_register.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/lfsr.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/lfsr_16bit.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/lfsr_8bit.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/lossy_valid_to_stream.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/mv_filter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/onehot_to_bin.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/plru_tree.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/passthrough_stream_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/popcount.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/rr_arb_tree.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/rstgen_bypass.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/serial_deglitch.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/shift_reg.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/shift_reg_gated.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/spill_register_flushable.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_demux.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_filter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_fork.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_intf.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_join_dynamic.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_mux.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_throttle.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/sub_per_hash.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/sync.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/sync_wedge.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/unread.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/read.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/addr_decode_dync.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_2phase.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_4phase.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/clk_int_div_static.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/addr_decode.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/addr_decode_napot.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/multiaddr_decode.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cb_filter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_fifo_2phase.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/clk_mux_glitch_free.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/counter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/ecc_decode.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/ecc_encode.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/edge_detect.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/lzc.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/max_counter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/rstgen.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/spill_register.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_delay.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_fork_dynamic.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_join.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_reset_ctrlr.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_fifo_gray.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/fall_through_register.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/id_queue.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_to_mem.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_arbiter_flushable.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_fifo_optimal_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_register.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_fifo_gray_clearable.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/cdc_2phase_clearable.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/mem_to_banks_detailed.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_arbiter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/stream_omega_net.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/mem_to_banks.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/sram.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/addr_decode_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/cb_filter_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/cdc_2phase_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/cdc_2phase_clearable_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/cdc_fifo_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/cdc_fifo_clearable_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/fifo_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/graycode_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/id_queue_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/passthrough_stream_fifo_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/popcount_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/rr_arb_tree_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/stream_test.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/stream_register_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/stream_to_mem_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/sub_per_hash_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/isochronous_crossing_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/stream_omega_net_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/stream_xbar_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/clk_int_div_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/clk_int_div_static_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/clk_mux_glitch_free_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/test/lossy_valid_to_stream_tb.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/clock_divider_counter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/clk_div.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/find_first_one.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/generic_LFSR_8bit.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/generic_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/prioarbiter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/pulp_sync.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/pulp_sync_wedge.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/rrarbiter.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/clock_divider.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/fifo_v2.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/deprecated/fifo_v1.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/edge_propagator_ack.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/edge_propagator.sv",
    f"{ROOT}/.bender/git/checkouts/common_cells-*/src/edge_propagator_rx.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_intf.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_err_slv.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_regs.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_cdc.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_demux.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/src/apb_test.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/test/tb_apb_regs.sv",
    f"{ROOT}/.bender/git/checkouts/apb-*/test/tb_apb_demux.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_intf.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_atop_filter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_burst_splitter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_burst_splitter_gran.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_burst_unwrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_fifo_delay_dyn.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_bus_compare.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_cdc_dst.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_cdc_src.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_cut.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_delayer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_demux_simple.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_dw_downsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_dw_upsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_id_remap.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_id_prepend.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_isolate.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_join.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_demux.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_dw_converter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_from_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_join.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_lfsr.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_mailbox.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_mux.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_regs.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_to_apb.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_to_axi.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_modify_address.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_mux.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_rw_join.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_rw_split.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_serializer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_slave_compare.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_throttle.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_detailed_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_cdc.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_demux.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_err_slv.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_dw_converter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_from_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_id_serialize.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lfsr.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_multicut.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_axi_lite.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_zero_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_interleaved_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_iw_converter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_lite_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_xbar_unmuxed.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_mem_banked.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_mem_interleaved.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_to_mem_split.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_xp.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_chan_compare.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_dumper.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_sim_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/src/axi_test.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_dw_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_xbar_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_addr_test.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_atop_filter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_bus_compare.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_cdc.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_delayer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_dw_downsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_dw_upsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_isolate.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_dw_converter.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_mailbox.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_regs.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_to_apb.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_to_axi.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_lite_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_modify_address.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_serializer.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_sim_mem.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_slave_compare.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_to_axi_lite.sv",
    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_to_mem_banked.sv",
#    f"{ROOT}/.bender/git/checkouts/axi-*/test/tb_axi_iw_converter.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/defs_div_sqrt_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/iteration_div_sqrt_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/control_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/norm_div_sqrt_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/preprocess_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/nrbd_nrsc_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/div_sqrt_top_mvp.sv",
    f"{ROOT}/.bender/git/checkouts/fpu_div_sqrt_mvp-*/hdl/div_sqrt_mvp_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_intf.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_rready_converter.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/apb_to_obi.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_atop_resolver.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_cut.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_demux.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_err_sbr.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_mux.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_sram_shim.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/obi_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/obi_asserter.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/obi_test.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/obi_sim_mem.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/tb_obi_xbar.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/atop_golden_mem_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/obi-*/src/test/tb_obi_atop_resolver.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/src/axi_stream_intf.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/src/axi_stream_cut.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/src/axi_stream_dw_downsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/src/axi_stream_dw_upsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/src/axi_stream_multicut.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/test/axi_stream_test.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/test/tb_axi_stream_dw_downsizer.sv",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/test/tb_axi_stream_dw_upsizer.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_cast_multi.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_classifier.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_divsqrt_th_64_multi.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/clk/rtl/gated_clk_cell.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_ctrl.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_ff1.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_pack_single.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_prepare.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_round_single.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_special.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_srt_single.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fdsu/rtl/pa_fdsu_top.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fpu/rtl/pa_fpu_dp.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fpu/rtl/pa_fpu_frbus.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/opene906/E906_RTL_FACTORY/gen_rtl/fpu/rtl/pa_fpu_src_type.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_ctrl.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_double.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_ff1.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_pack.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_prepare.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_round.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_scalar_dp.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_srt_radix16_bound_table.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_srt_radix16_with_sqrt.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_srt.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/vendor/openc910/C910_RTL_FACTORY/gen_rtl/vfdsu/rtl/ct_vfdsu_top.v",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_divsqrt_th_32.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_divsqrt_multi.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_fma.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_fma_multi.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_sdotp_multi.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_sdotp_multi_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_noncomp.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_opgroup_block.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_opgroup_fmt_slice.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_opgroup_multifmt_slice.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_rounding.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/lfsr_sr.sv",
    f"{ROOT}/.bender/git/checkouts/fpnew-*/src/fpnew_top.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_baudgen.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_interrupts.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_modem.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_rx.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_tx.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart_register.sv",
    f"{ROOT}/.bender/git/checkouts/obi_peripherals-*/hw/obi_uart/obi_uart.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_intf.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/vendor/lowrisc_opentitan/src/prim_subreg_arb.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/vendor/lowrisc_opentitan/src/prim_subreg_ext.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/apb_to_reg.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/axi_lite_to_reg.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/axi_to_reg_v2.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/periph_to_reg.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_cdc.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_cut.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_demux.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_err_slv.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_filter_empty_writes.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_mux.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_to_apb.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_to_mem.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_to_tlul.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_to_axi.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_uniform.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/vendor/lowrisc_opentitan/src/prim_subreg_shadow.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/vendor/lowrisc_opentitan/src/prim_subreg.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/deprecated/axi_to_reg.sv",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/src/reg_test.sv",
    f"{ROOT}/.bender/git/checkouts/apb_uart-*/src/apb_uart.sv",
    f"{ROOT}/.bender/git/checkouts/apb_uart-*/src/apb_uart_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/apb_uart-*/src/reg_uart_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_burst_cutter.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_data_way.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_merge_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_read_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_write_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_sram_data.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_sram_tag.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_index_assigner.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_trdl_index.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/eviction_refill/axi_llc_ax_master.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/eviction_refill/axi_llc_r_master.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/eviction_refill/axi_llc_w_master.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/hit_miss_detect/axi_llc_evict_box.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/hit_miss_detect/axi_llc_lock_box_bloom.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/hit_miss_detect/axi_llc_miss_counters.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/hit_miss_detect/axi_llc_tag_pattern_gen.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_chan_splitter.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_evict_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_refill_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_ways.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/hit_miss_detect/axi_llc_tag_store.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_config_pat.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_config_no_pat.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_config.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_hit_miss.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_top.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/src/axi_llc_reg_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/test/synth_axi_llc.sv",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/test/tb_axi_llc.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_res_tbl.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_amos_alu.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_amos.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_lrsc.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_atomics.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_lrsc_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_amos_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_atomics_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/axi_riscv_atomics-*/src/axi_riscv_atomics_structs.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/regs/axi_rt_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_gran_burst_splitter_counters.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_unit_counter.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_err_slv.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_regbus_guard.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/regs/axi_rt_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_gran_burst_splitter_ax_chan.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_gran_burst_splitter.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_write_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_unit.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_unit_top.sv",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/src/axi_rt_unit_top_synth.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/src/axi_vga_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/src/axi_vga_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/src/axi_vga_timing_fsm.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/src/axi_vga_fetcher.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/src/axi_vga.sv",
    f"{ROOT}/.bender/git/checkouts/axi_vga-*/test/tb_axi_vga.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicint_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicint_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicintv_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicintv_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicvs_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clicvs_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/mclic_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/mclic_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic_reg_adapter.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic_gateway.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic_target.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic_apb.sv",
    f"{ROOT}/.bender/git/checkouts/clic-*/src/clic.sv",
    f"{ROOT}/.bender/git/checkouts/clint-*/src/clint_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/clint-*/src/clint_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/clint-*/src/clint.sv",
    f"{ROOT}/.bender/git/checkouts/clint-*/test/clint_tb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/config_pkg.sv",
    "../../rtl/src/cv64a6_imafdcsclic_sv39_config_pkg.sv",
#    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/cv64a6_imafdcsclic_sv39_config_pkg.sv",
#    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/cv64a6_flamingo_config_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/riscv_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/ariane_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/build_config_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39/tlb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39/mmu.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39/ptw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_accel_first_pass_decoder_stub.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39x4/cva6_tlb_sv39x4.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39x4/cva6_mmu_sv39x4.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mmu_sv39x4/cva6_ptw_sv39x4.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_mmu/cva6_tlb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_mmu/cva6_shared_tlb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_mmu/cva6_mmu.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_mmu/cva6_ptw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_clic_controller.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/wt_cache_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/std_cache_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/acc_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/instr_tracer_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include/cvxif_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_example/include/cvxif_instr_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_fu.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_example/cvxif_example_coprocessor.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_example/instr_decoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_issue_register_commit_if_driver.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cvxif_compressed_if_driver.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/alu.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/fpu_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/branch_unit.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/compressed_decoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/controller.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/csr_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/csr_regfile.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/decoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/ex_stage.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/instr_realign.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/id_stage.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/issue_read_operands.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/issue_stage.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/load_unit.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/load_store_unit.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/lsu_bypass.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/mult.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/multiplier.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/serdiv.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/perf_counters.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/ariane_regfile_ff.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/ariane_regfile_fpga.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/scoreboard.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/raw_checker.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/store_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/amo_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/store_unit.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/commit_stage.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/axi_shim.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/acc_dispatcher.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_rvfi_probes.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cva6_fifo_v3.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/macro_decoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/bht2lvl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/btb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/bht.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/ras.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/instr_scan.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/instr_queue.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/frontend/frontend.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_dcache_ctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_dcache_mem.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_dcache_missunit.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_dcache_wbuffer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_dcache.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_icache.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_cache_subsystem.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/wt_axi_adapter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/ispm_ctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/dspm_ctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/tag_cmp.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cache_ctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/amo_alu.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/axi_adapter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/miss_handler.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/std_nbdcache.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_icache_axi_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/std_cache_subsystem.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/target/generic/hpdcache_params_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/utils/hpdcache_mem_resp_demux.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/utils/hpdcache_mem_to_axi_read.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/utils/hpdcache_mem_to_axi_write.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/utils/hpdcache_mem_req_read_arbiter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/utils/hpdcache_mem_req_write_arbiter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_demux.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_lfsr.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_sync_buffer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_fifo_reg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_fifo_reg_initialized.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_fxarb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_rrarb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_mux.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_decoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_1hot_to_binary.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_prio_1hot_encoder.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_sram.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_sram_wbyteenable.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_sram_wmask.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/macros/behav/hpdcache_sram_1rw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/macros/behav/hpdcache_sram_wmask_1rw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_regbank_wbyteenable_1rw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_regbank_wmask_1rw.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_data_downsize.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_data_upsize.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/common/hpdcache_data_resize.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hwpf_stride/hwpf_stride_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hwpf_stride/hwpf_stride.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hwpf_stride/hwpf_stride_arb.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hwpf_stride/hwpf_stride_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_amo.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_cmo.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_core_arbiter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_ctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_ctrl_pe.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_memctrl.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_miss_handler.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_mshr.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_mshr_to_cache_set.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_rtab.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_uncached.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_victim_plru.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_victim_random.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_victim_sel.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_wbuf.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_flush.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_memarray.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_wbuf_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/src/hpdcache_plru.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_hpdcache_if_adapter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_hpdcache_subsystem_axi_arbiter.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_hpdcache_subsystem.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/cva6_hpdcache_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache_tc_sram.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/pmp/src/pmp.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/pmp/src/pmp_entry.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/pmp/src/pmp_data_if.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/sram_pulp.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/sram_cache.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/tc_sram_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/tc_sram_wrapper_cache_techno.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/instr_tracer.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util/instr_tracer_if.sv",
    f"{ROOT}/.bender/git/checkouts/cva6-*/vendor/pulp-platform/fpga-support/fpga-support-stubs.sv",
#    f"{ROOT}/.bender/git/checkouts/dram_rtl_sim-*/src/sim_dram.sv",
#    f"{ROOT}/.bender/git/checkouts/dram_rtl_sim-*/src/axi_dram_sim.sv",
#    f"{ROOT}/.bender/git/checkouts/dram_rtl_sim-*/src/dram_sim_engine.sv",
#    f"{ROOT}/.bender/git/checkouts/dram_rtl_sim-*/test/axi_to_dram_tb.sv",
#    f"{ROOT}/.bender/git/checkouts/dram_rtl_sim-*/test/axi_to_multi_dram_tb.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/idma_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axil_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axil_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axi_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axi_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axis_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_axis_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_channel_coupler.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_dataflow_element.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_error_handler.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_init_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_init_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_legalizer_page_splitter.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_legalizer_pow2_splitter.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_obi_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_obi_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_tilelink_read.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/backend/idma_tilelink_write.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/target/rtl/idma_generated.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/midend/idma_mp_dist_midend.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/midend/idma_mp_split_midend.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/midend/idma_nd_midend.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/midend/idma_rt_midend.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_ar_gen.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_ar_gen_prefetch.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_reader.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_reader_gater.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_reshaper.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/idma_transfer_id_gen.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_reg_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/frontend/desc64/idma_desc64_top.sv",
    f"{ROOT}/.bender/git/checkouts/irq_router-*/rtl/irq_router_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/irq_router-*/rtl/irq_router_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/irq_router-*/rtl/irq_router.sv",
    f"{ROOT}/.bender/git/checkouts/irq_router-*/tb/irq_router_tb.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/prim_pulp_platform/prim_flop_2sync.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/prim_pulp_platform/prim_flop_en.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_fifo_sync_cnt.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_util_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_max_tree.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_sync_reqack.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_sync_reqack_data.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_pulse_sync.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_packer_fifo.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_fifo_sync.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_filter_ctr.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_intr_hw.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/prim/rtl/prim_fifo_async.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/gpio/rtl/gpio_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/rv_plic/rtl/rv_plic_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/gpio/rtl/gpio_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/rv_plic/rtl/rv_plic_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c_fsm.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/rv_plic/rtl/rv_plic_gateway.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_byte_merge.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_byte_select.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_cmd_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_command_queue.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_fsm.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_window.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_data_fifos.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_shift_register.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c_core.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/rv_plic/rtl/rv_plic_target.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host_core.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/gpio/rtl/gpio.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/i2c/rtl/i2c.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/spi_host/rtl/spi_host.sv",
    f"{ROOT}/.bender/git/checkouts/opentitan_peripherals-*/src/rv_plic/rtl/rv_plic.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/debug_rom/debug_rom.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/debug_rom/debug_rom_one_scratch.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_csrs.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_mem.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dmi_cdc.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dmi_jtag_tap.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_sba.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_top.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dmi_jtag.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dm_obi_top.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dmi_test.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/src/dmi_intf.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/tb/jtag_dmi/jtag_intf.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/tb/jtag_dmi/jtag_test.sv",
    f"{ROOT}/.bender/git/checkouts/riscv-dbg-*/tb/jtag_dmi/tb_jtag_dmi.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/regs/serial_link_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/regs/serial_link_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/regs/serial_link_single_channel_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/regs/serial_link_single_channel_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/channel_allocator/stream_chopper.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/channel_allocator/stream_dechopper.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/channel_allocator/channel_despread_sfr.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/channel_allocator/channel_spread_sfr.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/channel_allocator/serial_link_channel_allocator.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link_network.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link_data_link.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link_physical.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/serial_link_occamy_wrapper.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/axi_channel_compare.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/tb_axi_serial_link.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/tb_ch_calib_serial_link.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/tb_stream_chopper.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/tb_stream_chopper_dechopper.sv",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/test/tb_channel_allocator.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/bus_err_unit_bare.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/bus_err_unit_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/bus_err_unit_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/bus_err_unit.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/axi_err_unit_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/unbent-*/src/obi_err_unit_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/src/tagger_reg_reg_pkg.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/src/tagger_reg_reg_top.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/src/tagger.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/src/tagger_patid.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/src/tagger_regs_wrap.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/test/tb_tagger.sv",
    f"{ROOT}/.bender/git/checkouts/tagger-*/test/user_checker.sv",
    f"{ROOT}/hw/future/UsbOhciAxi4.v",
    f"{ROOT}/hw/future/spinal_usb_ohci.sv",
    f"{ROOT}/hw/regs/cheshire_reg_pkg.sv",
    f"{ROOT}/hw/regs/cheshire_reg_top.sv",
    f"{ROOT}/hw/cheshire_pkg.sv",
    f"{ROOT}/hw/bootrom/cheshire_bootrom.sv",
    f"{ROOT}/hw/cheshire_idma_wrap.sv",
    f"{ROOT}/hw/cheshire_soc.sv",
    f"{ROOT}/target/sim/models/s25fs512s.v",
    f"{ROOT}/target/sim/models/24FC1025.v",
    f"{ROOT}/target/sim/src/vip_cheshire_soc.sv",
    f"{ROOT}/target/sim/src/tb_cheshire_pkg.sv",
    f"{ROOT}/target/sim/src/fixture_cheshire_soc.sv",
    f"{ROOT}/target/sim/src/tb_cheshire_soc.sv",
    f"{ROOT}/target/sim/src/elfloader.cpp"
]

INC_DIRS = [
    f"{ROOT}/.bender/git/checkouts/common_cells-*/include",
    f"{ROOT}/.bender/git/checkouts/apb-*/include",
    f"{ROOT}/.bender/git/checkouts/axi-*/include",
    f"{ROOT}/.bender/git/checkouts/obi-*/include",
    f"{ROOT}/.bender/git/checkouts/axi_stream-*/include",
    f"{ROOT}/.bender/git/checkouts/register_interface-*/include",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/include",
    f"{ROOT}/.bender/git/checkouts/axi_llc-*/test",
    f"{ROOT}/.bender/git/checkouts/axi_rt-*/include",
    f"{ROOT}/.bender/git/checkouts/cva6-*/common/local/util",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/include",
    f"{ROOT}/.bender/git/checkouts/idma-*/src/include",
    f"{ROOT}/.bender/git/checkouts/idma-*/target/rtl/include",
    f"{ROOT}/.bender/git/checkouts/idma-*/test",
    f"{ROOT}/.bender/git/checkouts/serial_link-*/src/axis/include",
    f"{ROOT}/.bender/git/checkouts/tagger-*/include",
    f"{ROOT}/.bender/git/checkouts/cva6-*/core/cache_subsystem/hpdcache/rtl/include",
    f"{ROOT}/hw/include"
]

def run_test(simulator: str, test_file: Path, top_module: str, waves: bool, cfile: str):
    rtl_dir = Path(SCRIPT_DIR / "../../rtl")
    sim_dir = Path(SCRIPT_DIR / "../../rtl/sim")

    verilog_files = []
    for f in FILE_LIST:
        expanded = glob.glob(f)
        if expanded:
            verilog_files.extend(expanded)
        else:
            print(f"Warning: No files found for pattern {f}")
            #verilog_files.append(f)

    verilog_sources = (
        verilog_files
        + list(["../../rtl/header.vh"])
        + list(["../../rtl/src/cheshire_soc_wrap.sv"])
        + list(["../../rtl/src/ddr3_controller.sv"])
        + list(["../../rtl/src/ddr3_core.sv"])
        + list(["../../rtl/src/ddr3_dfi_phy.sv"])
        + list(["../../rtl/src/ddr3_dfi_seq.sv"])
        + list(["../../rtl/src/dram_wrapper.sv"])
        + list(["../../rtl/src/dram_controller_axi.sv"])
        + list(["../../rtl/src/dram_controller_wb.sv"])
        + list(["../../rtl/sim/ddr3.v"])
        + list(["../../rtl/vivado_ip/clk_wiz_0_sim_netlist.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/glbl.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/OBUFDS.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/IOBUFDS.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/OSERDESE2.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/ISERDESE2.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/IOBUF.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/IDELAYE2.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/IDELAYCTRL.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/BUFG.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/IBUFDS.v"])
        + list([f"{VIVADO_PATH}/data/verilog/src/unisims/MMCME2_ADV.v"])
    )

    #verilog_sources = list(dict.fromkeys(verilog_sources))

    vivado_ip_vhdls = [f"{VIVADO_PATH}/data/vhdl/src/unisims/unisim_VCOMP.vhd", f"{VIVADO_PATH}/data/vhdl/src/unisims/unisim_VPKG.vhd"]

    include_dirs = [
        #header.parent for header in verilog_sources
    ]

    expanded_inc_dirs = []
    for d in INC_DIRS:
        expanded = glob.glob(d)
        if expanded:
            expanded_inc_dirs.extend(expanded)
        else:
            print(f"Warning: No directories found for pattern {d}")
            #expanded_inc_dirs.append(d)

    include_dirs.extend(expanded_inc_dirs)

    include_dirs.extend([rtl_dir])
    include_dirs.extend([sim_dir])

    print("\nINCLUDE_DIRS:")
    print(include_dirs)
    print("\nVERILOG_SOURCES:")
    print(verilog_sources)

    import cocotb
    from cocotb.runner import Xcelium
    def fixed_test_command(self):
        self.env["CDS_AUTO_64BIT"] = "all"

        if self.pre_cmd:
            print("WARNING: pre_cmd is not implemented for Xcelium.")

        verbosity_opts = []
        if self.verbose:
            verbosity_opts += ["-messages", "-status", "-gverbose", "-pliverbose", "-plidebug", "-plierr_verbose"]
        else:
            verbosity_opts += ["-quiet", "-plinowarn"]

        tmpdir = f"implicit_tmpdir_{self.current_test_name}"
        xrun_top = ":" if self.hdl_toplevel_lang == "vhdl" else self.sim_hdl_toplevel

        input_script = (
            f"@database -open cocotb_waves -default;"
            f"probe -database cocotb_waves -create {xrun_top} -all -memories -variables -depth all;"
        #    f"probe -create -packed 131072 *;"
            f"run;"
            f"exit;"
            if self.waves
            else "@run; exit;"
        )

        cmds = [["mkdir", "-p", tmpdir]]
        cmds += [
            ["xrun"]
            + ["-logfile", f"xrun_{self.current_test_name}.log"]
            + ["-xmlibdirname", f"{self.build_dir}/xrun_snapshot"]
            + ["-cds_implicit_tmpdir", tmpdir]
            + ["-licqueue"]
            + verbosity_opts
            + ["-R"]
            + self.test_args
            + self.plusargs
            + (["-gui"] if self.gui else [])
            + ["-input", input_script]
        ]

        self.env["GPI_EXTRA"] = (
            cocotb.config.lib_name_path("vhpi", "xcelium") + ":cocotbvhpi_entry_point"
        )

        return cmds
    Xcelium._test_command = fixed_test_command

    runner_build_args = ["-modelsimini", "../../../vivado/modelsim.ini"]
    runner_pre_cmd = ['set WildcardFilter {};set WildcardSizeThreshold "16777216"; coverage save -onexit covres.ucdb;']
    runner_test_args = ["-suppress", "14408", "-suppress", "16154", "-suppress", "8630", "-modelsimini", "../../../vivado/modelsim.ini", "-L", "compiled-libs", "top.glbl"]

    if simulator.lower() == "xcelium":
        with open("pre_input.tcl", "w") as f:
            f.writelines(["set probe_packed_limit 0;\n", "set probe_unpacked_limit 0;\n"])
        if DRAM_SIM: #if "dram" in cfile:
            runner_build_args.extend(["-f", f"{VIVADO_PATH}/data/secureip/secureip_cell.list.f"])
        runner_build_args = [
                             #"-f", f"{VIVADO_PATH}/data/secureip/secureip_cell.list.f",
                             "-newperf", "-plusperf",
                             "-top", "glbl",
                             "-namemap_mixgen", "-verbose", "-access", "+rwc", "-timescale", "1ns/1ps", "-ALLOWREDEFINITION", "-relax", "-sv",
                             "-v93",
                             "+define+TARGET_CVA6",
                             "+define+TARGET_RTL",
                             "+define+TARGET_SIM",
                             "+define+TARGET_SIMULATION",
                             "+define+TARGET_TEST",
                             "+define+TARGET_VCS",
                             "+define+TARGET_CV64A6_FLAMINGO",
                             #"+define+TARGET_CV64A6_IMAFDCSCLIC_SV39",
        ] #'+incdir+"../../../vivado/cva_soc_zc706/cva_soc_zc706.gen/sources_1/ip/clk_wiz_0"']
        if DRAM_SIM: #if "dram" in cfile:
            runner_build_args.extend(["-f", f"{VIVADO_PATH}/data/secureip/secureip_cell.list.f"])
        runner_pre_cmd = []
        runner_test_args = ["-newperf", "-plusperf",
                            "-top", "glbl",
                            "-verbose", "-access", "+rwc", "-timescale", "1ns/1ps", "-pre_input", "../pre_input.tcl",
                            f"+BOOTMODE={BOOTMODE.__str__()} +PRELMODE={PRELMODE.__str__()} +BINARY={BINARY}"] #["set probe_packed_limit 131072; set probe_unpacked_limit 131072;"] #["probe -create -packed 131072 *;"]

    runner = get_runner(simulator)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vivado_ip_vhdls,
        includes=include_dirs,
        hdl_toplevel=top_module,
        always=True,
    #    build_args=["-L", "../../vivado/compiled-libs"]
    #    build_args=["-modelsimini", "../../../vivado/modelsim.ini"]
        build_args=runner_build_args
    )

    runner.test(
        hdl_toplevel=top_module,
    #    hdl_toplevel_library="glbl",
        hdl_toplevel_lang="verilog",
        test_module=str(test_file),
        waves=waves,
        gui=False,
        plusargs=["+nowarnTSCALE"],
        extra_env={
            "XILINX_VIVADO": VIVADO_PATH,
        #    "COCOTB_LOG_LEVEL": "TRACE",
        #    "COCOTB_SCHEDULER_DEBUG": "1",
            "SHM_RESET_DEFAULTS": "1",
        #    "SHM_UNPACKED_LIMIT": "131072",
        #    "SHM_PACKED_LIMIT": "131072",
        #    "CADENCE_ENABLE_AVSREQ_44905_PHASE_1": "1",
        #    "CADENCE_ENABLE_AVSREQ_63188_PHASE_1": "1",
            "COCOTB_HDL_TIMEUNIT": "1ns",
            "COCOTB_HDL_TIMEPRECISION": "1ps",
            "CFILE": cfile,
            "BINARY": BINARY,
            "BOOTMODE": BOOTMODE.__str__(),
            "PRELMODE": PRELMODE.__str__()
        },
        pre_cmd=runner_pre_cmd,
    #    pre_cmd=["probe -create -packed 131072 *;"]
        #pre_cmd=[
        #    'set WildcardFilter {};set WildcardSizeThreshold "16777216"; coverage save -onexit covres.ucdb;' #vmap compiled-libs "../../vivado/compiled-libs";'
        #],
        ##test_args=["-L", "compiled-libs"]
        ##test_args=["-L", "../../vivado/compiled-libs"]
        ##test_args=["-modelsimini ../../vivado/modelsim.ini"]
        #test_args=["-suppress", "14408", "-suppress", "16154", "-suppress", "8630", "-modelsimini", "../../../vivado/modelsim.ini", "-L", "compiled-libs", "top.glbl"]
        test_args=runner_test_args
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sim", type=str, help="Simulator. <icarus, verilator, questa>"
    )
    parser.add_argument(
        "--top", type=str, help="Top level hdl module to test a.k.a DUT"
    )
    parser.add_argument(
        "--test",
        type=str,
        help="Python test file to run, all tests inside will be run",
    )
    parser.add_argument("--waves", type=bool, help="Dump waves? <true,false>")

    parser.add_argument("--cfile", type=str, help="Test file to run")

    args = parser.parse_args()

    test_dir = Path(SCRIPT_DIR / "tb")
    tests = list(test_dir.rglob("*.py"))
    print("test_dir: ", test_dir)
    print("tests: ", tests)

    test_names = {test.stem: test for test in test_dir.rglob("*.py")}

    # if args.test not in test_names:
    #     raise FileNotFoundError(f"Can't find <{args.test}> in <{tests}>")

    try:
        run_test(args.sim, args.test, args.top, args.waves, args.cfile)
    except:
        pass
