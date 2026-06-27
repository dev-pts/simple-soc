LOP_HDL ?= python3 main.py

Top.v: king.lop
	$(LOP_HDL) gen-verilog $(TOP) $^ > Top.v

king.lop: Top.lop CPU.lop SimpleSRAM.lop UARTReceiver.lop Counter.lop ShiftRegister.lop ClkClk.lop UARTBootloader.lop UARTTransmitter.lop
	cat $^ > king.lop

clean:
	rm -f king.lop
	rm -f Top.v
