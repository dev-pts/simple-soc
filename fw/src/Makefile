CROSS = riscv64-unknown-elf-
CC = $(CROSS)gcc
OBJCOPY = $(CROSS)objcopy
OBJDUMP = $(CROSS)objdump

BUILD_DIR = build
RTOS_SOURCE_DIR = $(abspath ../FreeRTOS-Kernel)

CPPFLAGS = \
	-D__riscv_float_abi_soft \
	-I$(RTOS_SOURCE_DIR)/include \
	-I. \

CFLAGS = \
	-Wall \
	-mabi=ilp32 -mcmodel=medany \
	-ffunction-sections \
	-fdata-sections

CFLAGS += -march=rv32im

LDFLAGS = -nostartfiles -Tfw.lds \
	-march=rv32ima -mabi=ilp32 -mcmodel=medany \
	-Xlinker --gc-sections \
	-Xlinker --defsym=__stack_size=4096 \
	-Xlinker -Map=$(BUILD_DIR)/fw.map

CFLAGS += -Os

CFLAGS += --specs=picolibc.specs -DPICOLIBC_INTEGER_PRINTF_SCANF
LDFLAGS += --specs=picolibc.specs -DPICOLIBC_INTEGER_PRINTF_SCANF

CSRCS = \
	$(RTOS_SOURCE_DIR)/list.c \
	$(RTOS_SOURCE_DIR)/tasks.c \
	$(RTOS_SOURCE_DIR)/portable/MemMang/heap_3.c \
	port.c \
	main.c uart.c \

ASMS = \
	start.S \

OBJS = $(CSRCS:%.c=$(BUILD_DIR)/%.o) $(ASMS:%.S=$(BUILD_DIR)/%.o)
DEPS = $(CSRCS:%.c=$(BUILD_DIR)/%.d) $(ASMS:%.S=$(BUILD_DIR)/%.d)

all: $(BUILD_DIR)/fw.elf $(BUILD_DIR)/fw.bin $(BUILD_DIR)/fw.hex $(BUILD_DIR)/fw.lst

$(BUILD_DIR)/fw.elf: $(OBJS) fw.lds Makefile
	$(CC) $(LDFLAGS) $(OBJS) -o $@

$(BUILD_DIR)/fw.bin: $(BUILD_DIR)/fw.elf
	$(OBJCOPY) -O binary $^ $@

$(BUILD_DIR)/fw.hex: $(BUILD_DIR)/fw.elf
	xxd -e -c 4 $^ | cut -b 11-18 > $@

$(BUILD_DIR)/fw.lst: $(BUILD_DIR)/fw.elf
	$(OBJDUMP) -D $^ > $@

$(BUILD_DIR)/%.o: %.c Makefile
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c $< -o $@

$(BUILD_DIR)/%.o: %.S Makefile
	@mkdir -p $(@D)
	$(CC) $(CPPFLAGS) $(CFLAGS) -MMD -MP -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)

-include $(DEPS)
