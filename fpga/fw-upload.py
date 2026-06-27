import serial
import numpy as np
import sys, getopt
from time import sleep

def do_reset(ser):
	ser.open()

	# NOTE ser.send_break() does not work
	# So, emulate break by sending zero with slow speed
	ser.baudrate = 9600
	ser.write(b'\x00')
	ser.flush()

	ser.close()

def do_upload(ser, firmware):
	ser.baudrate = 2_000_000
	ser.open()

	with open(firmware, "r") as f:
		a = np.fromfile(f, dtype='>i4')

	for i in range(len(a)):
		print('Writing ' + str(i) + ' of ' + str(len(a)))
		ser.write(a[i].tobytes())
		ser.write(b'\x01')

	ser.close()

def do_release(ser):
	ser.baudrate = 2_000_000
	ser.open()

	ser.write(b'\x00\x00\x00\x00')
	ser.write(b'\x00')
	ser.flush()

	ser.close()

firmware = None
device = None

try:
	opts, args = getopt.getopt(sys.argv[1:], "d:f:r", [ "device=", "firmware=" ])
except getopt.GetoptError:
	sys.exit(2)

for opt, arg in opts:
	if opt in ("-f", "--firmware"):
		firmware = arg
	elif opt in ("-d", "--device"):
		device = arg

ser = serial.Serial()
ser.port = device
ser.timeout = None

do_reset(ser)
do_upload(ser, firmware)
do_release(ser)
