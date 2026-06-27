import numpy as np

import VeriTest

def task1(dut):
	p = dut.port

	p.clk = 1
	p.reset = 1
	dut.wait(10)

	p.reset = 0

	dut.semaphore()

	dut.dump(True)
	dut.wait(200000)
	dut.finish()

def task2(dut):
	p = dut.port

	uart = VeriTest.UART(dut, p.uart_in, 50_000_000 / 2_000_000)

	p.uart_in = 1
	p.reset.wait(0)

	# Assert reset
	uart.break_cond()

	with open('a.bin', 'r') as f:
		a = np.fromfile(f, dtype='>i4')

	for i in range(len(a)):
		print(int(i / len(a) * 100))
		uart.tx(a[i].tobytes())
		uart.tx(b'\x01')

	dut.semaphore()

	# Release reset
	uart.tx(b'\x00\x00\x00\x00')
	uart.tx(b'\x00')

vt = VeriTest.VeriTest(['clk', 'reset', 'uart_in'], 'simx.vcd')
vt.add(task1)
vt.add(task2)
vt.run()
