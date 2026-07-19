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
a = [ vt.add(param=0), vt.add(param=1) ]
d = [ vt.add(param=0), vt.add(param=1) ]
vt.start()

for i in range(len(a)):
	a[i].semaphore()
	d[i].semaphore()

def a_send(dut, addr, wen, size=0, cond=None):
	def task():
		p = dut.port
		idx = dut.param

		p.bus[idx].a.addr.set(addr)
		p.bus[idx].a.wen.set(wen)
		p.bus[idx].a.len.set(size)
		p.bus[idx].a.valid.set(1)

		p.clk.addwait(0)
		p.bus[idx].a.ready.addwait(1)
		dut.wait()

		dut.wait(1)
		p.bus[idx].a.valid.set(0)

		if cond:
			dut.cond_notify(cond)

	dut.ev.run(task)

def d_send(dut, data, strb, size=0, cond=None, wait_after_addr=0, cond_remove=False):
	def task():
		p = dut.port
		idx = dut.param

		if cond:
			dut.cond_wait(cond)

		if wait_after_addr:
			dut.wait(wait_after_addr)

		for i in range(size + 1):
			p.bus[idx].w.data.set(data + i)
			p.bus[idx].w.strb.set(strb)
			p.bus[idx].w.valid.set(1)

			p.clk.addwait(0)
			p.bus[idx].w.ready.addwait(1)
			dut.wait()

			p.clk.addwait(1)
			dut.wait()
			p.bus[idx].w.valid.set(0)

		if cond_remove:
			dut.cond_remove(cond)

	dut.ev.run(task)

def d_recv(dut, size=0, cond=None, wait_after_addr=-1, cond_remove=False, wait_after_each=0):
	def task():
		p = dut.port
		idx = dut.param

		if wait_after_addr >= 0:
			if cond:
				dut.cond_wait(cond)
			dut.wait(wait_after_addr)

		p.bus[idx].r.ready.set(1)

		for i in range(size + 1):
			p.clk.addwait(0)
			p.bus[idx].r.valid.addwait(1)
			dut.wait()
			p.clk.addwait(1)
			dut.wait()

			if wait_after_each:
				p.bus[idx].r.ready.set(0)
				dut.wait(wait_after_each)
				p.bus[idx].r.ready.set(1)

		p.bus[idx].r.ready.set(0)

		if cond_remove:
			dut.cond_remove(cond)

	dut.ev.run(task)

def write_addr_data_together(addr, size=0):
	for i in range(len(a)):
		a_send(a[i], addr, 1, size)
		d_send(d[i], addr, 0xf, size)

		a[i].ev.wait()
		d[i].ev.wait()

def write_addr_ack_data(addr, size=0, wait_after_addr=0):
	for i in range(len(a)):
		cond = next(cc)

		a_send(a[i], addr, 1, size, cond=cond)
		d_send(d[i], addr, 0xf, size, cond=cond, wait_after_addr=wait_after_addr, cond_remove=True)

		a[i].ev.wait()
		d[i].ev.wait()

def read_addr_data(addr, size=0, wait_after_addr=-1, wait_after_each=0):
	for i in range(len(a)):
		cond = next(cc)

		a_send(a[i], addr, 0, size, cond=cond if wait_after_addr >= 0 else None)
		d_recv(d[i], size, cond=cond, wait_after_addr=wait_after_addr, cond_remove=True, wait_after_each=wait_after_each)

		a[i].ev.wait()
		d[i].ev.wait()

def next_test():
	vt.wait(4)
	vt.semaphore(*a, *d)

def cond_creator():
	i = 0
	while True:
		yield str(i)
		i += 1

cc = cond_creator()

if True:
	write_addr_data_together(0x1)

	next_test()

if True:
	write_addr_ack_data(0x2)

	next_test()

if True:
	write_addr_ack_data(0x3, wait_after_addr=4)

	next_test()

if True:
	write_addr_data_together(0x2)
	write_addr_data_together(0x4)
	write_addr_data_together(0x6)
	write_addr_data_together(0x8)

	next_test()

if True:
	write_addr_ack_data(0x2)
	write_addr_ack_data(0x4)
	write_addr_ack_data(0x6)
	write_addr_ack_data(0x8)

	next_test()

if True:
	write_addr_data_together(0x4, 1)

	next_test()

if True:
	write_addr_ack_data(0x8, 1)

	next_test()

if True:
	write_addr_ack_data(0xc, 1, wait_after_addr=4)

	next_test()

if True:
	write_addr_data_together(0x10, 1)
	write_addr_data_together(0x14, 1)
	write_addr_data_together(0x18, 1)
	write_addr_data_together(0x1c, 1)

	next_test()

if True:
	write_addr_ack_data(0x20, 1)
	write_addr_ack_data(0x24, 1)
	write_addr_ack_data(0x28, 1)
	write_addr_ack_data(0x2c, 1)

	next_test()

if True:
	read_addr_data(0x1)

	next_test()

if True:
	read_addr_data(0x2, wait_after_addr=0)

	next_test()

if True:
	read_addr_data(0x3, wait_after_addr=6)

	next_test()

if True:
	read_addr_data(0x2)
	read_addr_data(0x4)
	read_addr_data(0x6)
	read_addr_data(0x8)

	next_test()

if True:
	read_addr_data(0x2, wait_after_addr=0)
	read_addr_data(0x4, wait_after_addr=0)
	read_addr_data(0x6, wait_after_addr=0)
	read_addr_data(0x8, wait_after_addr=0)

	next_test()

if True:
	read_addr_data(0x2, wait_after_addr=4)
	read_addr_data(0x4, wait_after_addr=4)
	read_addr_data(0x6, wait_after_addr=4)
	read_addr_data(0x8, wait_after_addr=4)

	next_test()

if True:
	read_addr_data(0x4, 1)

	next_test()

if True:
	read_addr_data(0x8, 1)

	next_test()

if True:
	read_addr_data(0xc, 1, wait_after_addr=4)

	next_test()

if True:
	read_addr_data(0x10, 1)
	read_addr_data(0x14, 1)
	read_addr_data(0x18, 1)
	read_addr_data(0x1c, 1)

	next_test()

if True:
	read_addr_data(0x20, 1, wait_after_addr=4, wait_after_each=2)
	read_addr_data(0x24, 1, wait_after_addr=4)
	read_addr_data(0x28, 1, wait_after_addr=4)
	read_addr_data(0x2c, 1, wait_after_addr=4)

	next_test()

for i in range(len(a)):
	a[i].ev.stop()
	d[i].ev.stop()

vt.finish()
