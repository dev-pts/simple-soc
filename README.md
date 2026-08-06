The CPU is RISC-V quark translated from https://github.com/BrunoLevy/learn-fpga from Verilog to LOP HDL (https://github.com/dev-pts/lop-hdl).

See build.sh for everything.

Example usage:
```
sh -xe build.sh build && sh -xe build.sh run test.py Top clk a.bin
sh -xe build.sh build && sh -xe build.sh run test.py Top clk ../fw/src/build/fw.bin
```
