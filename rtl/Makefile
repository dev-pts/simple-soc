LOP_HDL ?= python3 main.py

Top.v: king.lop
	$(LOP_HDL) gen-verilog $(TOP) $^ > Top.v

king.lop: $(filter-out king.lop,$(wildcard *.lop))
	cat $^ > $@

clean:
	rm -f king.lop
	rm -f Top.v
