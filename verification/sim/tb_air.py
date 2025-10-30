from random import getrandbits
from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.triggers import RisingEdge, FallingEdge, Edge, ClockCycles, Timer
from cocotbext.jtag import JTAGDriver, JTAGBus, JTAGDevice

## dummy patch
if not hasattr(Timer, 'cbhdl'):
    Timer.cbhdl = None

BINARY="../../../cheshire/sw/tests/helloworld.spm.elf"
BOOTMODE=0
PRELMODE=1

TIMEOUT = 2000000000
tests = {}

import os
cfile = os.environ['CFILE']

from pathlib import Path
SCRIPT_DIR = Path(os.path.realpath(__file__)).parent.absolute()
test_hex = {
    cfile: {
        "TEST_FILE": f"{SCRIPT_DIR}/../../tests/{cfile}/{cfile}.hex",
        "fail_adr": 0x40F00060,
        "pass_adr": 0x40F00078,
        "instructions": [],
    }
}
if cfile == "coremark":
    from tests import coremark
    tests.update(coremark)
else:
    tests.update(test_hex)

@cocotb.coroutine
async def uart_monitor(dut, clk, cpu_clk, baud_rate):
    # Calculate number of clock cycles per UART bit
    cycles_per_bit = int(cpu_clk / baud_rate)
    half_bit = cycles_per_bit // 2

    bit_time_ns = 1e9 / baud_rate
    half_bit_time_ns = bit_time_ns / 2

    bit_time_ns = int(bit_time_ns)
    half_bit_time_ns = int(half_bit_time_ns)

    print("UART Monitor started")
    while True:
        # Wait for start bit (falling edge)
        await FallingEdge(dut.uart_tx)
        # Wait half bit to sample in middle of first data bit
        #await ClockCycles(clk, half_bit)
        await Timer(half_bit_time_ns, 'ns')

        # Read 8 data bits
        data = 0
        for i in range(8):
            #await ClockCycles(clk, cycles_per_bit)
            await Timer(bit_time_ns, 'ns')
            bit = int(dut.uart_tx.value)
            data |= (bit << i)

        # Wait for stop bit
        #await ClockCycles(clk, cycles_per_bit)
        await Timer(bit_time_ns, 'ns')

        # Convert to character
        try:
            char = chr(data)
        except ValueError:
            char = '?'

        # Print to console like a terminal
        print(char, end='', flush=True)
        ### reset if Done dram write
        #if(char == 'e'):
        #    print()
        #    dut.rst_ni.value = 0
        #    await RisingEdge(clk)
        #    dut.rst_ni.value = 1
        #    #break

@cocotb.coroutine
async def read_instructions():
    for test in tests:
        with open(tests[test]["TEST_FILE"], "r") as f:
            instructions = [line.rstrip("\n") for line in f]
        tests[test]["instructions"] = instructions

def load_verilog_hex_file():
    for test in tests:
        with open(tests[test]["TEST_FILE"].replace(".hex", ".vmem"), "r") as file:
            lines = file.readlines()

        memory = {}
        current_address = None

        for line in lines:
            if line.startswith("@"):
                current_address = int(line[1:], 16)
            else:
                values = line.strip().split()
                for value in values:
                    if current_address is not None:
                        memory[current_address] = int(value, 16)
                        current_address += 1

    return memory

def load_dram_verilog_hex_file():
    for test in tests:
        #with open(tests[test]["TEST_FILE"].rsplit("/", 2)[0] + "/coremark/coremark_baremetal.vmem", "r") as file:
        #with open(tests[test]["TEST_FILE"].rsplit("/", 2)[0] + "/demo/demo.vmem", "r") as file:
        #with open(tests[test]["TEST_FILE"].rsplit("/", 2)[0] + "/atomics/atomics.vmem", "r") as file:
        #with open(tests[test]["TEST_FILE"].replace(".hex", ".vmem"), "r") as file:
        with open("/home/shc/projects/clones/riscv-opensbi-port/build/platform/template/firmware/fw_dynamic.vmem", "r") as file:
        #with open("/home/shc/projects/temp/tekno-kizil/testler/riscv-tests/isa/rv32ua-p-lrsc_static.hex", "r") as file:
            lines = file.readlines()

        memory = {}
        current_address = None

        for line in lines:
            if line.startswith("@"):
                current_address = int(line[1:], 16) - 0x80000000  # Adjust for DRAM base address
            else:
                values = line.strip().split()
                for value in values:
                    if current_address is not None:
                        memory[current_address] = int(value, 16)
                        current_address += 1

    return memory

def load_dram_hex_file():
    for test in tests:
        with open(tests[test]["TEST_FILE"].rsplit("/", 2)[0] + "/demo/demo.hex", "r") as file:
            lines = file.readlines()

        memory = {}
        address = 0

        for line in lines:
            line = line.strip()
            if line:
                word = int(line, 16)
                for i in range(4):
                    byte_val = (word >> (i * 8)) & 0xFF
                    memory[address + i] = byte_val
                address += 4

    return memory

def extract_address_fields(addr, BA_BITS, ROW_BITS, COL_BITS):
    col_mask = (1 << COL_BITS) - 1
    col = addr & col_mask

    row_mask = (1 << ROW_BITS) - 1
    row = (addr >> COL_BITS) & row_mask

    bank_mask = (1 << BA_BITS) - 1
    bank = (addr >> (ROW_BITS + COL_BITS)) & bank_mask

    return bank, row, col

def extract_address_fields_rbc(addr, BA_BITS, ROW_BITS, COL_BITS):
    col_mask = (1 << COL_BITS) - 1
    col = addr & col_mask

    bank_mask = (1 << BA_BITS) - 1
    bank = (addr >> COL_BITS) & bank_mask

    row_mask = (1 << ROW_BITS) - 1
    row = (addr >> (COL_BITS + BA_BITS)) & row_mask

    return row, bank, col

IR_DMI = 0x11
DMI_DMCONTROL_ADDR = 0x10
DMI_DMSTATUS_ADDR = 0x11
DMI_DATA0_ADDR = 0x04
DMI_COMMAND_ADDR = 0x17
DMI_OP_WRITE = 2
DMI_OP_READ = 1
DMI_OP_NOP = 0

DMI_REG_NAME = "DMI_REG"

class RiscvDebug:
    def __init__(self, jtag_driver: JTAGDriver, device_num: int):
        self.jtag = jtag_driver
        self.log = jtag_driver.log
        self.dev_num = device_num

    async def dmi_op(self, addr, op, data):
        dmi_packet = (op << 40) | (data << 8) | (addr << 1) | DMI_OP_NOP

        await self.jtag.write(DMI_REG_NAME, dmi_packet, device=self.dev_num)
        tdo = self.jtag.ret_val

        if op == DMI_OP_WRITE:
            return 0
        else:
            op_status = tdo & 0b11
            if op_status != 0:
                self.log.error(f"DMI operation failed! Status: {op_status}")
            return (tdo >> 2) & 0xFFFFFFFF

    async def dmi_write(self, addr, data):
        await self.dmi_op(addr, DMI_OP_WRITE, data)

    async def dmi_read(self, addr):
        return await self.dmi_op(addr, DMI_OP_READ, 0)

    async def halt_core(self):
        await self.dmi_write(DMI_DMCONTROL_ADDR, 0x80000001)
        for _ in range(10):
            status = await self.dmi_read(DMI_DMSTATUS_ADDR)
            if status & (1 << 9):
                self.log.info("Core is halted.")
                return
        self.log.error("Failed to halt core.")

    async def resume_core(self):
        await self.dmi_write(DMI_DMCONTROL_ADDR, 0x40000001)
        self.log.info(f"Resuming core...")

    async def write_memory_word(self, address, data):
        await self.dmi_write(DMI_DATA0_ADDR, address)
        await self.dmi_write(DMI_DATA0_ADDR + 1, data)
        command = (2 << 20) | (1 << 17) | (1 << 16)
        await self.dmi_write(DMI_COMMAND_ADDR, command)
        for _ in range(10):
            status = await self.dmi_read(DMI_DMSTATUS_ADDR)
            if (status >> 10) & 0b111 == 0:
                self.log.info(f"Data 0x{data:08X} is written to address 0x{address:08X}")
                return
        self.log.error(f"Write memory command failed for address 0x{address:08X}")

@cocotb.coroutine
async def test_write_scratch_regs_via_jtag(dut, clk):
    jtag_bus = JTAGBus(
        entity=dut,
        signals={"tck": "jtag_tck", "tms": "jtag_tms", "tdi": "jtag_tdi", "tdo": "jtag_tdo", "trst": "jtag_trst_n"}
    )
    jtag_driver = JTAGDriver(bus=jtag_bus, period=100, unit="ns")

    riscv_debug_device = JTAGDevice(ir_len=5)
    riscv_debug_device.add_jtag_reg(name=DMI_REG_NAME, width=42, address=IR_DMI)
    jtag_driver.add_device(riscv_debug_device)

    debugger = RiscvDebug(jtag_driver, device_num=0)

    dut.rst_ni.value = 0
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    dut.rst_ni.value = 1

    await jtag_driver.set_reset(1)
    await jtag_driver.reset_finished()
    await jtag_driver.set_reset(0)
    await jtag_driver.reset_fsm()

    await debugger.halt_core()

    await debugger.write_memory_word(0x03000000, 0x80000000)
    await debugger.write_memory_word(0x03000004, 0x00000000)
    await debugger.write_memory_word(0x03000008, 2)

    await debugger.resume_core()

    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)
    await RisingEdge(clk)

timeout = 0

import signal
def signal_handler(sig, frame):
    global timeout
    timeout = TIMEOUT
    pass

signal.signal(signal.SIGINT, signal_handler)

@cocotb.coroutine
async def main_memory(dut, clk, start_address):
    await RisingEdge(clk)
    dut.rst_ni.value = 0
    await RisingEdge(clk)
    dut.rst_ni.value = 1

    global timeout
    while True:
        try:
            await RisingEdge(clk)
            if timeout > TIMEOUT:
                break
            timeout += 1
        except:
            pass

@cocotb.test()
async def tair(dut):
    dut.boot_mode_i.value = BOOTMODE

    #bus = JTAGBus(
    #    entity=dut,
    #    signals={
    #        "tck": "jtag_tck",
    #        "tms": "jtag_tms",
    #        "tdi": "jtag_tdi",
    #        "tdo": "jtag_tdo",
    #        "trst": "jtag_trst_n"
    #    }
    #)
    #jtag_driver = JTAGDriver(bus)
    #jtag_driver.add_device(JTAGDevice())

    ## start address of hex file not boot address
    ## boot address is 0x80 always but the hex file start address can be different
    start_address = 0x00000000
    ## is not used now

    clk_ns = 5
    baud_rate = 115200

    if hasattr(dut, "clk_p") and hasattr(dut, "clk_n"):
        clk_ns = 5
        # drive the positive pin
        clk = dut.clk_p
        cocotb.start_soon(Clock(clk, clk_ns, "ns").start(start_high=False))

        # in parallel, tie clk_n to the inverse of clk_p
        async def drive_inverted():
            # initialise
            dut.clk_n.value = 1
            while True:
                await RisingEdge(clk)
                dut.clk_n.value = 0
                await FallingEdge(clk)
                dut.clk_n.value = 1

        cocotb.start_soon(drive_inverted())

    else:
        # fallback to single-ended
        clk = dut.clk
        cocotb.start_soon(Clock(clk, clk_ns, "ns").start(start_high=False))

    dut.rst_ni.value = 0
    await RisingEdge(clk)
    await RisingEdge(clk)
    dut.rst_ni.value = 1

    #await jtag_driver.write(0x03000000, 0x80000000)
    #await jtag_driver.write(0x03000004, 0x00000000)
    #await jtag_driver.write(0x03000008, 2)

    setjtag = cocotb.start_soon(test_write_scratch_regs_via_jtag(dut, clk))
    await setjtag

    cocotb.start_soon(uart_monitor(dut, clk, clk_ns, baud_rate))
    blk = cocotb.start_soon(main_memory(dut, clk, start_address))
    await blk
    print()
