LOP_HDL ?= python3 main.py
TB_CPP ?= tb.cpp
GEN_TB_H ?= sh gen-tb-h.sh
TEST ?= test.py
VERI_TEST ?= VeryTest.py

tb: $(TB_CPP) TopSim.v
	$(VERILATOR) --trace-underscore --no-timing --x-initial-edge --cc --trace -Wno-lint --exe --build -O3 --x-assign fast --x-initial fast --noassert -Wno-fatal --top $(TOP) \
		-CFLAGS "-I$(PWD)" \
		--build-jobs $(shell nproc) \
		$^

run: a.bin
	PYTHONPATH=$(dir $(VERI_TEST)) python3 $(TEST) obj_dir/V$(TOP)

a.bin: a.c
	sh build.sh build

TopSim.v: king.lop
	$(LOP_HDL) gen-verilog $(TOP) $^ > TopSim.v
	$(GEN_TB_H) $(TOP) $^

clean:
	rm -fr __pycache__
	rm -fr obj_dir/
	rm -f tb-sig.h tb-top.h tb.py
	rm -f TopSim.v
	rm -f king.lop
	rm -f simx.vcd
	sh build.sh clean
