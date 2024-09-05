# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: MIT

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_shift(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut.select.value = 1
    dut.latch_add.value = 1
    dut.latch_and.value = 1

    for i in range(16):
        dut.data_in.value = i & 1
        await ClockCycles(dut.clk, 1)
