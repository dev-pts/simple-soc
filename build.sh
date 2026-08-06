#!/bin/sh

clean() {
	cd tools/list-o-pad/
	make clean
	cd -

	cd tools/lop-hdl/
	make clean
	cd -

	cd rtl/
	make clean
	cd -

	cd fw/src
	make clean
	cd -

	cd sim/
	make clean
	cd -
}

build() {
	cd tools/list-o-pad/
	make
	cd -

	cd tools/lop-hdl/
	make LOP=$(pwd)/../list-o-pad
	cd -

	cd rtl/
	make Top.v \
		LOP_HDL="python3 ../tools/lop-hdl/main.py" \
		TOP=Top
	cd -

	cd fw/src
	make
	cd -

	cd sim/
	make a.bin \
		CROSS_COMPILE=${HOME}/opt/cross/bin/riscv-elf-
	cd -
}

run() {
	cp rtl/king.lop sim/

	cd sim/
	make tb \
		VERILATOR=../../verilator/bin/verilator \
		TB_CPP=$(pwd)/../tools/veri-test/tb.cpp \
		LOP_HDL="python3 ../tools/lop-hdl/main.py" \
		GEN_TB_H="sh $(pwd)/../tools/veri-test/gen-tb-h.sh" \
		VERI_TEST=$(pwd)/../tools/veri-test/VeriTest.py \
		TOP=$2 \
		CLK=$3

	make run \
		VERI_TEST=$(pwd)/../tools/veri-test/VeriTest.py \
		TEST=$1 \
		TOP=$2 \
		FWBIN=$4

	cd -
}

cmd=$1
shift

$cmd $@
