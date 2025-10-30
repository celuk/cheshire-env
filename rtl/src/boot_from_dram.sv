module boot_from_dram import cheshire_reg_pkg::*; #(
  parameter type reg_ext_req_t      = logic,
  parameter type reg_ext_rsp_t      = logic
)(
  input logic clk_i,
  input logic rst_ni,

  input  reg_ext_req_t  reg_req_i,
  output reg_ext_rsp_t  reg_rsp_o
);

    localparam logic [31:0] BASE_REGS_ADDR = 32'h0300_0000;
    localparam logic [63:0] DRAM_ENTRY_POINT = 64'h80000000;

    typedef enum logic [2:0] {
        IDLE,
        WRITE_SCRATCH0,
        WRITE_SCRATCH1,
        WRITE_SCRATCH2,
        DONE
    } state_e;

    state_e state_q, state_d;

    always_ff @(posedge clk_i or negedge rst_ni) begin
        if (!rst_ni) begin
            state_q <= IDLE;
        end else begin
            state_q <= state_d;
        end
    end

    always_comb begin
        state_d   = state_q;
        reg_rsp_o = '0;

        case (state_q)
            IDLE: begin
                if (reg_req_i.valid) begin
                    state_d = WRITE_SCRATCH0;
                end
            end

            WRITE_SCRATCH0: begin
                reg_rsp_o.ready = 1'b1;

                if (reg_req_i.valid && reg_req_i.write && reg_req_i.addr == (BASE_REGS_ADDR + CHESHIRE_SCRATCH_0_OFFSET)) begin
                    state_d = WRITE_SCRATCH1;
                end
            end

            WRITE_SCRATCH1: begin
                reg_rsp_o.ready = 1'b1;

                if (reg_req_i.valid && reg_req_i.write && reg_req_i.addr == (BASE_REGS_ADDR + CHESHIRE_SCRATCH_1_OFFSET)) begin
                    state_d = WRITE_SCRATCH2;
                end
            end

            WRITE_SCRATCH2: begin
                reg_rsp_o.ready = 1'b1;

                if (reg_req_i.valid && reg_req_i.write && reg_req_i.addr == (BASE_REGS_ADDR + CHESHIRE_SCRATCH_2_OFFSET)) begin
                    state_d = DONE;
                end
            end

            DONE: begin
                state_d = DONE;
            end

            default: state_d = IDLE;
        endcase
    end

endmodule
