#!/bin/sh

build() {
	${CROSS_COMPILE}gcc \
		-march=rv32i -mabi=ilp32 \
		-nostdlib -fno-PIC -ffreestanding \
		-Xlinker --gc-sections \
		-Xlinker -Ttext=0 \
		-Wall \
		-Os \
		-std=gnu11 \
		a.c \

	${CROSS_COMPILE}objcopy -O binary a.out a.bin
	xxd -e -c 2 a.bin | cut -d ' ' -f 2 > a.hex
	${CROSS_COMPILE}objdump -M numeric,no-aliases -D a.out > a.lst
}

clean() {
	rm -f a.bin a.o a.hex a.out a.lst
}

$1
