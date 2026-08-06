#define REGSIZE 4
#define LOAD lw
#define STOR sw

	.section .init
	.globl _start
	.type _start, @function
_start:
	.cfi_startproc
	.cfi_undefined ra
	.option push
	.option norelax
	la gp, __global_pointer$
	.option pop

	la sp, _stack_top

	// Load data section
	la a0, _data_lma
	la a1, _data
	la a2, _edata
	bgeu a1, a2, 2f

1:
	LOAD t0, (a0)
	STOR t0, (a1)
	addi a0, a0, REGSIZE
	addi a1, a1, REGSIZE
	bltu a1, a2, 1b

2:
	// Clear bss section
	la a0, _bss
	la a1, _ebss
	bgeu a0, a1, 2f

1:
	STOR zero, (a0)
	addi a0, a0, REGSIZE
	bltu a0, a1, 1b

2:
	// argc, argv, envp is 0
	li a0, 0
	li a1, 0
	li a2, 0
	jal main

1:
	j 1b
	.cfi_endproc

	.macro portStackRegister op
	\op x1, 0 * REGSIZE(sp)
	\op x5, 1 * REGSIZE(sp)
	\op x6, 2 * REGSIZE(sp)
	\op x7, 3 * REGSIZE(sp)
	\op x8, 4 * REGSIZE(sp)
	\op x9, 5 * REGSIZE(sp)
	\op x10, 6 * REGSIZE(sp)
	\op x11, 7 * REGSIZE(sp)
	\op x12, 8 * REGSIZE(sp)
	\op x13, 9 * REGSIZE(sp)
	\op x14, 10 * REGSIZE(sp)
	\op x15, 11 * REGSIZE(sp)
	\op x16, 12 * REGSIZE(sp)
	\op x17, 13 * REGSIZE(sp)
	\op x18, 14 * REGSIZE(sp)
	\op x19, 15 * REGSIZE(sp)
	\op x20, 16 * REGSIZE(sp)
	\op x21, 17 * REGSIZE(sp)
	\op x22, 18 * REGSIZE(sp)
	\op x23, 19 * REGSIZE(sp)
	\op x24, 20 * REGSIZE(sp)
	\op x25, 21 * REGSIZE(sp)
	\op x26, 22 * REGSIZE(sp)
	\op x27, 23 * REGSIZE(sp)
	\op x28, 24 * REGSIZE(sp)
	\op x29, 25 * REGSIZE(sp)
	\op x30, 26 * REGSIZE(sp)
	\op x31, 27 * REGSIZE(sp)
	.endm

	.extern pxCurrentTCB

	.section .text

	.globl xPortSwitchToTask
xPortSwitchToTask:
	call vTaskSwitchContext

	LOAD t1, pxCurrentTCB
	LOAD sp, 0(t1)

	portStackRegister LOAD

	addi sp, sp, REGSIZE * 28
	ret

	.globl vPortYield
vPortYield:
	addi sp, sp, -REGSIZE * 28

	portStackRegister STOR

	LOAD t1, pxCurrentTCB
	STOR sp, 0(t1)

	j xPortSwitchToTask
