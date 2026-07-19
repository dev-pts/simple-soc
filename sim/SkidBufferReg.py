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
m = vt.add()
s = vt.add()
vt.start()

def s_send(dut, data):
	def task():
		p = dut.port

		p.slave.data.set(data)
		p.slave.valid.set(1)

		p.clk.addwait(0)
		p.slave.ready.addwait(1)
		dut.wait()

		p.clk.addwait(1)
		dut.wait()
		p.slave.valid.set(0)

	dut.ev.run(task)

def m_recv(dut):
	def task():
		p = dut.port

		p.master.ready.set(1)

		p.clk.addwait(0)
		p.master.valid.addwait(1)
		dut.wait()

		p.clk.addwait(1)
		dut.wait()
		p.master.ready.set(0)

	dut.ev.run(task)

def next_test():
	vt.wait(4)
	vt.semaphore(m, s)

def cond_creator():
	i = 0
	while True:
		yield str(i)
		i += 1

cc = cond_creator()

m.semaphore()
s.semaphore()

if True:
	s_send(s, 0x1)
	m_recv(m)

	s.ev.wait()
	m.ev.wait()

	next_test()

if True:
	s_send(s, 0x2)

	m.wait(10)
	m_recv(m)

	s.ev.wait()
	m.ev.wait()

	next_test()

if True:
	s_send(s, 0x3)
	s_send(s, 0x4)
	s_send(s, 0x5)
	s_send(s, 0x6)

	m.wait(2)
	m_recv(m)
	m_recv(m)
	m_recv(m)
	m_recv(m)

	s.ev.wait()
	m.ev.wait()

	next_test()

if True:
	s_send(s, 0x3)
	s_send(s, 0x4)
	s_send(s, 0x5)
	s_send(s, 0x6)

	m.ev.run(lambda: m.wait(6))
	m_recv(m)
	m_recv(m)
	m.ev.run(lambda: m.wait(6))
	m_recv(m)
	m_recv(m)

	s.ev.wait()
	m.ev.wait()

	next_test()

m.ev.stop()
s.ev.stop()

vt.finish()
