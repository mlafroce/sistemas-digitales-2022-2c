import pytest
import glob
import cocotb
from cocotb_test.simulator import run
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

GREEN_TIME = 30
YELLOW_TIME = 3

'''
1. Testbench
'''
@cocotb.test()
async def simple_test(dut):
    ''' Clock Generation '''
    clock = Clock(dut.clk, 20, units="ns") # create a 50Mhz clock for dut.clk pin
    cocotb.start_soon(clock.start()) # start clock in a seperate thread

    for i in range(0, 20):
        await RisingEdge(dut.clk)
        assert dut.clk_out.value == (i % 5 == 0 and i != 0)
    

@pytest.mark.parametrize(
    "parameters", [
        {"DIVISOR": "5"},
    ])
def test_divisor(parameters):
    run(
        verilog_sources=glob.glob('clock_divisor.sv'),
        toplevel="clock_divisor",
        
        module="test_divisor",
        simulator="icarus",

        parameters=parameters,
        extra_env=parameters,
        sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )
