`timescale 1ns / 1ps

`include "header.vh"

module uart_programmer (
   input clk_i,
   input rst_ni,

   input logic program_rx_i
   ,output logic system_reset_o
   ,output logic prog_mode_led_o

   // New outputs for DRAM programming
   ,output logic dram_write_we_o,
   output logic [31:0] dram_write_addr_o,
   output logic [31:0] dram_write_data_o,
   output logic dram_write_rst_o,
   output logic dram_mode_o
);

   localparam CPU_CLK   = `CPU_CLK;
   localparam BAUD_RATE = `BAUD_RATE;

   localparam RESET_SEQUENCE    = "RESETTTTT";

   // Programming state machine signals
   localparam DRAMWRITE_SEQUENCE  = "DRAMWRITE";
   localparam PROG_SEQ_LENGTH     = 9;
   localparam SEQ_BREAK_THRESHOLD = 32'hffffffff; //32'd1000000;
   
   reg [PROG_SEQ_LENGTH*8-1:0] received_sequence;
   reg soft_rst;
   always @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
         soft_rst <= 1'b0;
      end else begin
         soft_rst <= (received_sequence == RESET_SEQUENCE);
      end
   end
   
   // =========================================================================
   // PROGRAMMING CONTROLLER 
   // =========================================================================
   
   // Signals for DRAMWRITE programming
   reg [31:0] dram_prog_size;
   reg [31:0] dram_prog_ctr;
   reg [31:0] dram_prog_addr;
   reg [31:0] dram_prog_instruction;
   reg dram_prog_inst_valid;
   reg dram_prog_sys_rst_n;
   
   reg [3:0] rcv_seq_ctr;
   reg [31:0] sequence_break_ctr;
   wire sequence_break = sequence_break_ctr == SEQ_BREAK_THRESHOLD;
   
   wire [31:0] prog_uart_do;
   wire ram_prog_rd_en;
   
   localparam SequenceWait           = 4'b0000;
   localparam SequenceReceive        = 4'b0001;
   localparam SequenceCheck          = 4'b0011;
   localparam SequenceDramWriteLengthCalc = 4'b1010;
   localparam SequenceDramWriteAddrCalc   = 4'b1011;
   localparam SequenceDramWriteProgram    = 4'b1110;
   localparam SequenceDramWriteFinish     = 4'b1100;
   
   reg [3:0] state_prog;
   reg [3:0] state_prog_next;
   reg [1:0] instruction_byte_ctr;
   
   always @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
        state_prog <= SequenceWait;
      end
      else if(soft_rst) begin
        state_prog <= SequenceWait;
      end
      else begin
        state_prog <= state_prog_next;
      end
   end

   always @(*) begin
      state_prog_next = state_prog;
      case (state_prog)
        SequenceWait: begin
          if (prog_uart_do != ~0) begin
            state_prog_next = SequenceReceive;
          end
        end
        SequenceReceive: begin
          if (prog_uart_do != ~0) begin
            if (rcv_seq_ctr == PROG_SEQ_LENGTH-1) begin
              state_prog_next = SequenceCheck;
            end
          end else if (sequence_break) begin
            state_prog_next = SequenceWait;
          end
        end
        SequenceCheck: begin
          if (received_sequence == DRAMWRITE_SEQUENCE) begin
            state_prog_next = SequenceDramWriteLengthCalc;
          end else begin
            state_prog_next = SequenceWait;
          end
        end
        SequenceDramWriteLengthCalc: begin
          if ((prog_uart_do != ~0) && &instruction_byte_ctr) begin
            state_prog_next = SequenceDramWriteAddrCalc;
          end
        end
        SequenceDramWriteAddrCalc: begin
          if ((prog_uart_do != ~0) && &instruction_byte_ctr) begin
            state_prog_next = SequenceDramWriteProgram;
          end
        end
        SequenceDramWriteProgram: begin
          if (dram_prog_ctr == dram_prog_size) begin
            state_prog_next = SequenceDramWriteFinish;
          end
        end
        SequenceDramWriteFinish: begin
          state_prog_next = SequenceWait;
        end
        default: begin
        end
      endcase
   end

   always @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
        instruction_byte_ctr <= 2'b0;
        sequence_break_ctr   <= 32'h0;
        received_sequence    <= 72'h0;
        rcv_seq_ctr          <= 4'h0;
        dram_prog_size       <= 32'h0;
        dram_prog_ctr        <= 32'h0;
        dram_prog_addr       <= 32'h0;
        dram_prog_instruction<= 32'h0;
        dram_prog_inst_valid <= 1'b0;
        dram_prog_sys_rst_n  <= 1'b1;
      end
      else if(soft_rst) begin
        instruction_byte_ctr <= 2'b0;
        sequence_break_ctr   <= 32'h0;
        received_sequence    <= 72'h0;
        rcv_seq_ctr          <= 4'h0;
        dram_prog_size       <= 32'h0;
        dram_prog_ctr        <= 32'h0;
        dram_prog_addr       <= 32'h0;
        dram_prog_instruction<= 32'h0;
        dram_prog_inst_valid <= 1'b0;
        dram_prog_sys_rst_n  <= 1'b1;
      end
      else begin
        dram_prog_inst_valid <= 1'b0;
        dram_prog_sys_rst_n <= 1'b1;
        
        if (dram_write_we_o) begin
          dram_prog_addr <= dram_prog_addr + 'h4;
        end
        
        case (state_prog)
          SequenceWait: begin
            instruction_byte_ctr <= 2'b0;
            sequence_break_ctr   <= 32'h0;
            received_sequence    <= 72'h0;
            rcv_seq_ctr          <= 4'h0;
            dram_prog_size       <= 32'h0;
            dram_prog_ctr        <= 32'h0;
            dram_prog_addr       <= 32'h0;
            dram_prog_instruction<= 32'h0;
            dram_prog_inst_valid <= 1'b0;
            dram_prog_sys_rst_n  <= 1'b1;
            if (prog_uart_do != ~0) begin
              rcv_seq_ctr <= rcv_seq_ctr + 4'h1;
              received_sequence <= {received_sequence[PROG_SEQ_LENGTH*8-9:0],prog_uart_do[7:0]};
            end
          end
          SequenceReceive: begin
            if (prog_uart_do != ~0) begin
              received_sequence <= {received_sequence[PROG_SEQ_LENGTH*8-9:0],prog_uart_do[7:0]};
              if (rcv_seq_ctr == PROG_SEQ_LENGTH-1) begin
                rcv_seq_ctr <= 4'h0;
              end else begin
                rcv_seq_ctr <= rcv_seq_ctr + 4'h1;
              end
            end else begin
              if (sequence_break) begin
                sequence_break_ctr <= 32'h0;
                rcv_seq_ctr        <= 4'h0;
              end else begin
                sequence_break_ctr <= sequence_break_ctr + 32'h1;
              end
            end
          end
          SequenceCheck: begin
            instruction_byte_ctr <= 2'b0;
          end
          SequenceDramWriteLengthCalc: begin
            dram_prog_ctr <= 32'h0;
            dram_prog_addr <= 32'h0;
            if (prog_uart_do != ~0) begin
              dram_prog_size <= {dram_prog_size[3*8-1:0],prog_uart_do[7:0]};
              if (&instruction_byte_ctr) begin
                instruction_byte_ctr <= 2'b0;
              end else begin
                instruction_byte_ctr <= instruction_byte_ctr + 2'b1;
              end
            end
          end
          SequenceDramWriteAddrCalc: begin
            if (prog_uart_do != ~0) begin
              dram_prog_addr <= {dram_prog_addr[3*8-1:0],prog_uart_do[7:0]};
              if (&instruction_byte_ctr) begin
                instruction_byte_ctr <= 2'b0;
              end else begin
                instruction_byte_ctr <= instruction_byte_ctr + 2'b1;
              end
            end
          end
          SequenceDramWriteProgram: begin
            if (prog_uart_do != ~0) begin
              dram_prog_instruction <= {dram_prog_instruction[3*8-1:0],prog_uart_do[7:0]};
              if (&instruction_byte_ctr) begin
                instruction_byte_ctr <= 2'b0;
                dram_prog_inst_valid <= 1'b1;
                dram_prog_ctr        <= dram_prog_ctr + 32'h1;
              end else begin
                instruction_byte_ctr <= instruction_byte_ctr + 2'b1;
                dram_prog_inst_valid <= 1'b0;
              end
            end else begin
              dram_prog_inst_valid <= 1'b0;
            end
          end
          SequenceDramWriteFinish: begin
            dram_prog_sys_rst_n <= 1'b0;
          end
          default: begin
          end
        endcase
      end
   end

   // Output assignments
   assign prog_mode_led_o = 1'b0;
   assign system_reset_o = dram_prog_sys_rst_n;
   assign ram_prog_rd_en = (state_prog != SequenceDramWriteFinish);

   // New DRAM output assignments
   assign dram_write_we_o   = dram_prog_inst_valid;
   assign dram_write_addr_o = dram_prog_addr;
   assign dram_write_data_o = dram_prog_instruction;
   assign dram_write_rst_o  = !dram_prog_sys_rst_n;
   assign dram_mode_o = (state_prog == SequenceDramWriteProgram);
   
   // =========================================================================
   // UART FOR PROGRAMMING
   // =========================================================================
   
   simpleuart #(
     .DEFAULT_DIV(CPU_CLK/BAUD_RATE)
   )
   simpleuart (
      .clk         (clk_i),
      .resetn      (rst_ni),
      .ser_tx      (),
      .ser_rx      (program_rx_i),
      .reg_div_we  (4'h0),
      .reg_div_di  (32'h0),
      .reg_div_do  (),
      .reg_dat_we  (1'b0),
      .reg_dat_re  (ram_prog_rd_en),
      .reg_dat_di  (32'h0),
      .reg_dat_do  (prog_uart_do)
   );

   initial begin
      state_prog = SequenceWait;
      instruction_byte_ctr = 2'b0;
      sequence_break_ctr = 32'h0;
      received_sequence = 72'h0;
      rcv_seq_ctr = 4'h0;
      dram_prog_size       = 32'h0;
      dram_prog_ctr        = 32'h0;
      dram_prog_addr       = 32'h0;
      dram_prog_instruction= 32'h0;
      dram_prog_inst_valid = 1'b0;
      dram_prog_sys_rst_n  = 1'b1;
   end

endmodule
