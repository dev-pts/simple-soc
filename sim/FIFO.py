import VeriTest
import tb

def task1(dut):
	p = dut.port

	p.clk.set(1)
	p.reset.set(1)
	dut.wait(10)

	dut.dump(True)

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

def cond_creator():
	i = 0
	while True:
		yield str(i)
		i += 1

cc = cond_creator()

def next_test():
	vt.wait(10)
	vt.semaphore(w, r)

wdata = 1

def write(dut, count=1, cond=None):
	def task():
		global wdata
		p = dut.port

		for i in range(count):
			p.wr.data.set(wdata)
			p.wr.valid.set(1)

			p.clk.addwait(0)
			p.wr.ready.addwait(1)
			dut.wait()

			dut.wait(1)
			p.wr.valid.set(0)

			wdata += 1

		if cond:
			dut.cond_notify(cond)

	dut.ev.run(task)
	dut.ev.wait()

def read(dut, count=1, cond=None):
	def task():
		p = dut.port

		if cond:
			dut.cond_wait(cond)

		for i in range(count):
			p.rd.ready.set(1)

			p.clk.addwait(0)
			p.rd.valid.addwait(1)
			dut.wait()

			dut.wait(1)
			p.rd.ready.set(0)

	dut.ev.run(task)
	dut.ev.wait()

def whole_test(prio_rd):
	global wdata

	w.port.prio_rd.set(prio_rd)

	wdata = 0x1

	if True:
		write(w)
		vt.wait(4)
		read(r)

		next_test()

	if True:
		cond = next(cc)

		write(w, 4, cond)
		read(r, 4, cond)

		next_test()

	if True:
		write(w, 4)
		read(r, 4)

		next_test()

	if True:
		cond = next(cc)

		write(w, 2, cond)
		write(w, 2)
		read(r, 4, cond)

		next_test()

	if True:
		write(w, 8)
		vt.wait(14)
		read(r, 8)

		next_test()

	if True:
		cond = next(cc)

		write(w)
		w.wait(2)
		write(w)
		w.wait(2)
		write(w)
		w.wait(2)
		write(w, cond=cond)

		r.cond_wait(cond)
		r.wait(6)

		read(r)
		r.wait(6)
		read(r)
		r.wait(2)
		read(r)
		r.wait(2)
		read(r)

		next_test()

	if True:
		write(w)
		w.wait(2)
		write(w)
		w.wait(2)
		write(w)
		w.wait(2)
		write(w)

		read(r, 4)

		next_test()

whole_test(0)
whole_test(1)

w.ev.stop()
r.ev.stop()

vt.finish()
