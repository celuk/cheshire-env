from random import getrandbits
from typing import Any, Dict, List

import cocotb
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.triggers import RisingEdge, FallingEdge, Edge, ClockCycles, Timer

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

timeout = 0

import signal
def signal_handler(sig, frame):
    global timeout
    timeout = TIMEOUT
    pass

signal.signal(signal.SIGINT, signal_handler)

@cocotb.coroutine
async def main_memory(dut, clk, start_address):
    dut.vip.set_boot_mode(BOOTMODE)
    dut.vip.wait_for_reset()
    exit_code = 0

    if BOOTMODE == 0:
        # Idle boot: preload with the specified mode
        if PRELMODE == 0:
            # JTAG mode
            print("[Boot] Using JTAG preload mode")
            dut.vip.jtag_init()
            dut.vip.jtag_elf_run(BINARY)
            await dut.vip.jtag_wait_for_eoc(exit_code)
        elif PRELMODE == 1:
            # Serial Link mode
            print("[Boot] Using Serial Link preload mode")
            dut.vip.slink_elf_run(BINARY)
            await dut.vip.slink_wait_for_eoc(exit_code)
        elif PRELMODE == 2:
            # UART mode
            print("[Boot] Using UART preload mode")
            await dut.vip.uart_debug_elf_run_and_wait(BINARY, exit_code)
        else:
            raise ValueError(f"Unsupported preload mode {PRELMODE} (reserved)!")
    elif BOOTMODE == 1:
        raise ValueError(f"Unsupported boot mode {BOOTMODE} (SD Card)!")
    else:
        # Autonomous boot: Only poll return code
        print("[Boot] Using autonomous boot mode")
        dut.vip.jtag_init()
        await dut.vip.jtag_wait_for_eoc(exit_code)
    
    # Wait for the UART to finish reading the current byte
    while True:
        try:
            await dut.vip.uart_reading_byte == 0
            if timeout > TIMEOUT:
                break
            timeout += 1
        except:
            pass
    
    #print(f"\n[Test] Completed with exit code: {exit_code}")
    #
    #if exit_code != 0:
    #    raise cocotb.result.TestFailure(f"Test failed with exit code {exit_code}")

@cocotb.test()
async def tair(dut):
    #await read_instructions()

    ## start address of hex file not boot address
    ## boot address is 0x80 always but the hex file start address can be different
    start_address = 0x00000000
    ## is not used now

    clk_ns = 5
    baud_rate = 115200

    #if hasattr(dut, "clk_p") and hasattr(dut, "clk_n"):
    #    clk_ns = 5
    #    # drive the positive pin
    #    clk = dut.clk_p
    #    cocotb.start_soon(Clock(clk, clk_ns, "ns").start(start_high=False))
#
    #    # in parallel, tie clk_n to the inverse of clk_p
    #    async def drive_inverted():
    #        # initialise
    #        dut.clk_n.value = 1
    #        while True:
    #            await RisingEdge(clk)
    #            dut.clk_n.value = 0
    #            await FallingEdge(clk)
    #            dut.clk_n.value = 1
#
    #    cocotb.start_soon(drive_inverted())
#
    #else:
    #    # fallback to single-ended
    #    clk = dut.clk
    #    cocotb.start_soon(Clock(clk, clk_ns, "ns").start(start_high=False))

    #dut.rst_ni.value = 0
    #await RisingEdge(clk)
    #await RisingEdge(clk)
    #dut.rst_ni.value = 1
    cocotb.start_soon(uart_monitor(dut, dut.clk, clk_ns, baud_rate))
    blk = cocotb.start_soon(main_memory(dut, dut.clk, start_address))
    await blk
    print()
