# SPDX-FileCopyrightText: © 2024 Michael Bell
# SPDX-License-Identifier: MIT

import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_shift(dut):
    dut._log.info("Start")

    # Set the clock period to 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await ClockCycles(dut.clk, 2, False)

    dut.rst_n.value = 1
    dut.select.value = 0
    dut.latch_add.value = 0
    dut.latch_and.value = 0

    for i in range(8):
        dut.data_in.value = (i & 1)
        await ClockCycles(dut.clk, 1, False)

    assert dut.uo_out.value == 0b01010101

    for i in range(8):
        dut.data_in.value = (~i & 1)
        await ClockCycles(dut.clk, 1, False)

    assert dut.uo_out.value == 0b10101010
    dut.select.value = 1
    await Timer(1, "ns")
    assert dut.uo_out.value == 0b01010101
    dut.select.value = 0

    reg_val = 0b0101010110101010

    for i in range(256):
        bit_in = random.randint(0, 1)
        dut.data_in.value = bit_in
        reg_val = ((reg_val << 1) | bit_in) & 0xFFFF
        await ClockCycles(dut.clk, 1, False)

        assert dut.uo_out.value == reg_val & 0xFF
        dut.select.value = 1
        await Timer(1, "ns")
        assert dut.uo_out.value == reg_val >> 8
        dut.select.value = 0

@cocotb.test()
async def test_add(dut):
    dut._log.info("Start")

    # Set the clock period to 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await ClockCycles(dut.clk, 2, False)

    dut.rst_n.value = 1
    dut.select.value = 2
    dut.latch_add.value = 1
    dut.latch_and.value = 0

    dut.data_in.value = 0
    await ClockCycles(dut.clk, 16, False)

    reg_val = 0
    for i in range(256):
        bit_in = random.randint(0, 1)
        dut.data_in.value = bit_in
        prev_reg_val = reg_val
        reg_val = ((reg_val << 1) | bit_in) & 0xFFFF
        await ClockCycles(dut.clk, 1, False)

        assert dut.uo_out.value == ((prev_reg_val & 0xFF) + (prev_reg_val >> 8)) & 0xFF

    latched_value = ((prev_reg_val & 0xFF) + (prev_reg_val >> 8)) & 0xFF

    for i in range(256):
        bit_in = random.randint(0, 1)
        latch = random.randint(0, 1)
        
        dut.data_in.value = bit_in
        dut.latch_add.value = latch

        prev_reg_val = reg_val
        reg_val = ((reg_val << 1) | bit_in) & 0xFFFF
        await ClockCycles(dut.clk, 1, False)

        if latch:
            latched_value = ((prev_reg_val & 0xFF) + (prev_reg_val >> 8)) & 0xFF
        assert dut.uo_out.value == latched_value

@cocotb.test()
async def test_and(dut):
    dut._log.info("Start")

    # Set the clock period to 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await ClockCycles(dut.clk, 2, False)

    dut.rst_n.value = 1
    dut.select.value = 3
    dut.latch_add.value = 0
    dut.latch_and.value = 1

    dut.data_in.value = 0
    await ClockCycles(dut.clk, 16, False)

    reg_val = 0
    for i in range(256):
        bit_in = random.randint(0, 1)
        dut.data_in.value = bit_in
        prev_reg_val = reg_val
        reg_val = ((reg_val << 1) | bit_in) & 0xFFFF
        await ClockCycles(dut.clk, 1, False)

        assert dut.uo_out.value == ((prev_reg_val & 0xFF) & (prev_reg_val >> 8))

    latched_value = ((prev_reg_val & 0xFF) & (prev_reg_val >> 8))

    for i in range(256):
        bit_in = random.randint(0, 1)
        latch = random.randint(0, 1)
        
        dut.data_in.value = bit_in
        dut.latch_and.value = latch

        prev_reg_val = reg_val
        reg_val = ((reg_val << 1) | bit_in) & 0xFFFF
        await ClockCycles(dut.clk, 1, False)

        if latch:
            latched_value = ((prev_reg_val & 0xFF) & (prev_reg_val >> 8))
        assert dut.uo_out.value == latched_value


@cocotb.test()
async def test_loopback(dut):
    dut._log.info("Start")

    # Set the clock period to 10 ns (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # When under reset: ui_in -> uo_out
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)

    for i in range(256):
        dut.ui_in.value = i
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == i
