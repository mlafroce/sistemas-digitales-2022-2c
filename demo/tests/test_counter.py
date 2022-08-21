import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

from cocotb_test.simulator import run
import pytest
import glob


@pytest.mark.parametrize(
    "parameters", [
        {"N": "16"},
    ])
def test_semaphore(parameters):
    print("Running...")
    run(
        verilog_sources=glob.glob('./*.sv'),
        #vhdl_sources=glob.glob('./*.vhdl'),
        toplevel="counter",    # top level HDL
        
        module="test_counter", # name of the file that contains @cocotb.test() -- this file
        simulator="icarus",
        #simulator="ghdl",

        parameters=parameters,
        extra_env=parameters,
        sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
        )

'''
Tests
'''

@cocotb.test()
async def counter_enable(dut):
    print("Running async...")

    ''' Clock Generation '''
    clock = Clock(dut.clk, 10, units="ms") # create a clock for dut.clk pin with 10 ns period
    cocotb.start_soon(clock.start()) # start clock in a seperate thread
    expected = 0

    for i in range(100): # 100 experiments
        enabled = i > 50 and i < 70
        dut.enabled = enabled
        if enabled:
            expected += 1
        
        await FallingEdge(dut.clk) # wait for falling edge
        
        computed = dut.count.value.integer # Read pins as unsigned integer.
        print(f"Computed: {computed}")
        # computed = dut.q.value.signed_integer # Read pins as signed integer.
        
        assert expected == computed, f"Failed on the {i}th cycle. Got {computed}, expected {expected}" # If any assertion fails, the test fails, and the string would be printed in console
        print(f"Driven value: {expected} \t received value: {computed}") 
