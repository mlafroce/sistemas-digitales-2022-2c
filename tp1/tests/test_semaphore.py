import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, FallingEdge, ClockCycles

GREEN_TIME = 30
YELLOW_TIME = 3

class Semaphore:
    def __init__(self, dut):
        self.dut = dut
        self.elapsed = 0

        self.green1 = False
        self.yellow1 = False
        self.red1 = False
        self.green2 = False
        self.yellow2 = False
        self.red2 = False

    async def run_seconds(self, seconds):
        self.elapsed += seconds
        self.elapsed = self.elapsed % ((GREEN_TIME + YELLOW_TIME) * 2)
        self.update_status()

        for i in range(0, seconds):
            await RisingEdge(self.dut.dbg_seconds)

    def update_status(self):
        if self.elapsed < YELLOW_TIME:
            self.yellow1 = self.yellow2 = True
            self.green1 = self.green2 = self.red1 = self.red2 = False
        elif self.elapsed < (YELLOW_TIME + GREEN_TIME):
            self.green1 = self.red2 = True
            self.yellow1 = self.green2 = self.red1 = self.yellow2 = False
        elif self.elapsed < (YELLOW_TIME + GREEN_TIME + YELLOW_TIME):
            self.yellow1 = self.yellow2 = True
            self.green1 = self.green2 = self.red1 = self.red2 = False
        else:
            self.green2 = self.red1 = True
            self.yellow1 = self.green1 = self.red2 = self.yellow2 = False
        
    def assert_status(self):
        assert(self.green1 == self.dut.green1.value)
        assert(self.yellow1 == self.dut.yellow1.value)
        assert(self.red1 == self.dut.red1.value)
        assert(self.green2 == self.dut.green2.value)
        assert(self.yellow2 == self.dut.yellow2.value)
        assert(self.red2 == self.dut.red2.value)


'''
1. Testbench
'''
@cocotb.test()
async def simple_test(dut):
    print("Running async...")

    ''' Clock Generation '''
    clock = Clock(dut.clk, 20, units="ns") # create a 50Mhz clock for dut.clk pin
    cocotb.start_soon(clock.start()) # start clock in a seperate thread

    ''' Assert clean init '''
    semaphore = Semaphore(dut)
    semaphore.assert_status()
    
    ''' Starts with yellow on both sides '''
    await semaphore.run_seconds(2)
    semaphore.assert_status()

    ''' Green 1 on, Red 2 on, others off '''
    await semaphore.run_seconds(30)
    semaphore.assert_status()
    
    ''' Yellow on both sides '''
    await semaphore.run_seconds(3)
    semaphore.assert_status()

    ''' Green 2 on, Red 1 on, others off '''
    await semaphore.run_seconds(30)
    semaphore.assert_status()
    
    ''' Yellow on both sides '''
    await semaphore.run_seconds(3)
    semaphore.assert_status()

'''
2. Pytest Setup
'''

from cocotb_test.simulator import run
import pytest
import glob


@pytest.mark.parametrize(
    "parameters", [
        {"GREEN_SECS": "30", "YELLOW_SECS": "3"},
    ])
def test_semaphore(parameters):
    print("Running...")
    run(
        verilog_sources=glob.glob('./*.sv'),
        toplevel="semaphore",    # top level HDL
        
        module="test_semaphore", # name of the file that contains @cocotb.test() -- this file
        simulator="icarus",

        parameters=parameters,
        extra_env=parameters,
        sim_build="sim_build/" + ",".join((f"{key}={value}" for key, value in parameters.items())),
    )