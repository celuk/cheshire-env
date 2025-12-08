module tc_sram #(
  parameter int unsigned NumWords     = 32'd1024,
  parameter int unsigned DataWidth    = 32'd128,
  parameter int unsigned ByteWidth    = 32'd8,
  parameter int unsigned NumPorts     = 32'd2,
  parameter int unsigned Latency      = 32'd1,
  parameter              SimInit      = "none",
  parameter bit          PrintSimCfg  = 1'b0,
  parameter              ImplKey      = "none",
  // DEPENDENT PARAMETERS
  parameter int unsigned AddrWidth = (NumWords > 32'd1) ? $clog2(NumWords) : 32'd1,
  parameter int unsigned BeWidth   = (DataWidth + ByteWidth - 32'd1) / ByteWidth,
  parameter type         addr_t    = logic [AddrWidth-1:0],
  parameter type         data_t    = logic [DataWidth-1:0],
  parameter type         be_t      = logic [BeWidth-1:0]
) (
  input  logic                 clk_i,
  input  logic                 rst_ni,
  input  logic  [NumPorts-1:0] req_i,
  input  logic  [NumPorts-1:0] we_i,
  input  addr_t [NumPorts-1:0] addr_i,
  input  data_t [NumPorts-1:0] wdata_i,
  input  be_t   [NumPorts-1:0] be_i,
  output data_t [NumPorts-1:0] rdata_o
);

  addr_t r_addr_q [NumPorts-1:0];

  always_ff @(posedge clk_i) begin
    for (int i = 0; i < NumPorts; i++) begin
      if (~rst_ni) begin
        r_addr_q[i] <= '0;
      end else begin
        // Update hold address only on a Read Request
        if (req_i[i] && !we_i[i]) begin
          r_addr_q[i] <= addr_i[i];
        end
      end
    end
  end

  addr_t [NumPorts-1:0] addr_mux;
  always_comb begin
    for (int i = 0; i < NumPorts; i++) begin
      addr_mux[i] = (req_i[i] && !we_i[i]) ? addr_i[i] : r_addr_q[i];
    end
  end
  
  genvar p, b;
  generate
    for (p = 0; p < NumPorts; p++) begin : gen_ports
      for (b = 0; b < BeWidth; b++) begin : gen_byte_lanes
      
        localparam int unsigned LOW_BIT  = b * ByteWidth;
        localparam int unsigned HIGH_BIT = ((b + 1) * ByteWidth > DataWidth) ? 
                                           DataWidth - 1 : 
                                           (b + 1) * ByteWidth - 1;
        localparam int unsigned WIDTH    = HIGH_BIT - LOW_BIT + 1;

        (* ram_style = "block" *) logic [WIDTH-1:0] mem_slice [NumWords-1:0];
        logic [WIDTH-1:0] r_data_slice;
        
        always_ff @(posedge clk_i) begin
          // Write Logic
          if (req_i[p] && we_i[p]) begin
            if (be_i[p][b]) begin
              mem_slice[addr_i[p]] <= wdata_i[p][HIGH_BIT:LOW_BIT];
            end
          end
          
          // Read Logic
          r_data_slice <= mem_slice[addr_mux[p]];
        end

        if (Latency > 1) begin : gen_lat
           logic [WIDTH-1:0] pipe_regs [Latency-1:1];
           always_ff @(posedge clk_i or negedge rst_ni) begin
             if (~rst_ni) begin
               for (int k=1; k<Latency; k++) pipe_regs[k] <= '0;
             end else begin
               pipe_regs[1] <= r_data_slice;
               for (int k=2; k<Latency; k++) pipe_regs[k] <= pipe_regs[k-1];
             end
           end
           assign rdata_o[p][HIGH_BIT:LOW_BIT] = pipe_regs[Latency-1];
           
        end else if (Latency == 1) begin : gen_lat1
           assign rdata_o[p][HIGH_BIT:LOW_BIT] = r_data_slice;
           
        end else begin : gen_lat0
           assign rdata_o[p][HIGH_BIT:LOW_BIT] = (req_i[p] && !we_i[p]) ? 
                                                 mem_slice[addr_i[p]] : 
                                                 mem_slice[r_addr_q[p]];
        end
      end
    end
  endgenerate

endmodule: tc_sram
