# Cocotb library mini-demo

## Files

* *counter.sv*: verilog definition of a counter with `clock`, `enabled` and `reset` inputs. The output is a N-width array.

* *counter.vhdl*: VHDL equivalent of counter.sv.

* *tests/test_counter*: tests written in python using `cocotb` and `cocotb-test`. Since `cocotb-test` uses `pytest`, we will use pytest name convention for tests discovery.

* *Makefile*: Makefile with useful commands

## Setup

Install Icarus Verilog compiler if you are planning to develop in verilog language:

```
sudo apt install iverilog
```

or install GHDL if you are planning to develop in VHDL

```
sudo apt install ghdl
```

```
pip install cocotb cocotb-test
```

It is also recommended to install `gtk-wave` for waveform visualization

## Execute

Run `make test` to execute pytest on verilog modules

You can comment `verilog_sources` and uncomment `vhdl_sources` to test VHDL implementation. Remember to change `simulator="icarus"` to ghdl

## Notes

*Icarus* simulator has a default timescale of 1 second, which means that we cannot simulate smaller time steps. We can override this timescale adding the next line to our top HDL element

```
`timescale 1ns/1ns
```

## References

* Verilog or VHDL: https://www.fpga4student.com/2017/08/verilog-vs-vhdl-explain-by-example.html
* Cocotb: https://docs.cocotb.org/en/stable/quickstart.htm
* Cocotb-test: https://github.com/themperek/cocotb-test