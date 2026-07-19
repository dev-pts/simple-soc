import VeriTest
import tb

def task1(dut):
	p = dut.port

	dut.dump(True)

	p.clk.set(1)
	p.reset.set(1)
	dut.wait(10)

	p.reset.set(0)
	dut.wait(2)

	dut.semaphore()

	dut.wait(1000)
	dut.finish()

vt = VeriTest.VeriTest(tb.ports, 'simx.vcd')
vt.add(task1)
w = vt.add()
r = vt.add()
vt.start()

w.semaphore()
r.semaphore()

def next_test():
	vt.wait(4)
	vt.semaphore(w, r)

def write(dut, data):
	def task():
		p = dut.port

		p.wr.data.set(data)
		p.wr.valid.set(1)

		p.clk.addwait(0)
		p.wr.ready.addwait(1)
		dut.wait()

		dut.wait(1)
		p.wr.valid.set(0)

	dut.ev.run(task)
	dut.ev.wait()

def read(dut):
	def task():
		p = dut.port

		p.rd.ready.set(1)

		p.clk.addwait(0)
		p.rd.valid.addwait(1)
		dut.wait()

		dut.wait(1)
		p.rd.ready.set(0)

	dut.ev.run(task)
	dut.ev.wait()

if True:
	write(w, 0x1)

	next_test()

if True:
	read(r)

	next_test()

if True:
	write(w, 0x2)
	w.wait(2)
	write(w, 0x3)
	w.wait(2)
	write(w, 0x4)
	w.wait(2)
	write(w, 0x5)

	next_test()

if True:
	read(r)
	r.wait(2)
	read(r)
	r.wait(2)
	read(r)
	r.wait(2)
	read(r)

	next_test()

w.ev.stop()
r.ev.stop()

vt.finish()
