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
		TOP=$2

	make run \
		VERI_TEST=$(pwd)/../tools/veri-test/VeriTest.py \
		CROSS_COMPILE=${HOME}/opt/cross/bin/riscv-elf- \
		TEST=$1 \
		TOP=$2

	cd -
}

$1 $2 $3
