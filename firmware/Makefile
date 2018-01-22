include ../include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

ifeq ($(PLATFORM),)
$(error PLATFORM not defined.)
endif
UPLATFORM = $(shell echo $(PLATFORM) | tr a-z A-Z)

ifeq ($(TARGET),)
$(error TARGET not defined.)
endif
UTARGET = $(shell echo $(TARGET) | tr a-z A-Z)

CFLAGS += -DPLATFORM_$(UPLATFORM) -DTARGET_$(UTARGET)

BUILD_DIRECTORY=$(BUILDINC_DIRECTORY)/../../
FIRMBUILD_DIRECTORY=$(BUILD_DIRECTORY)/software/firmware

OBJECTS=\
	isr.o \
	main.o \
	boot-helper-$(CPU).o


CFLAGS += \
	-I$(FIRMWARE_DIRECTORY) \
	-I$(BUILD_DIRECTORY)/software/firmware

CFLAGS += \
	-Wall \
	-Werror \
	-Wno-error=unused-function \
	-Wno-error=unused-variable \


include $(UIP_DIRECTORY)/Makefile.mk

LDFLAGS += \

all: firmware.bin firmware.fbi

%.fbi: %.bin
	$(PYTHON) -m litex.soc.tools.mkmscimg -f $< -o $@

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@
	chmod -x $@

firmware.elf: $(FIRMWARE_DIRECTORY)/linker.ld $(OBJECTS)

%.elf: ../libbase/crt0-$(CPU).o ../libbase/libbase-nofloat.a ../libcompiler_rt/libcompiler_rt.a ../uip/libuip.a
	$(LD) $(LDFLAGS) \
		-T $(FIRMWARE_DIRECTORY)/linker.ld \
		-N -o $@ \
                ../libbase/crt0-$(CPU).o \
                $(OBJECTS) \
                -L../libbase \
		-lbase-nofloat \
                -L../libcompiler_rt \
		-lcompiler_rt \
		-L../uip \
		-luip
	chmod -x $@

# pull in dependency info for *existing* .o files
-include $(OBJECTS:.o=.d)

boot-helper-$(CPU).S: $(BIOS_DIRECTORY)/boot-helper-$(CPU).S
	cp $< $@

%.o: $(FIRMWARE_DIRECTORY)/%.c
	$(compile)

%.o: $(FIRMWARE_DIRECTORY)/%.S
	$(assemble)

clean:
	$(RM) $(OBJECTS) $(OBJECTS:.o=.d) firmware.elf firmware.bin .*~ *~

.PHONY: all clean libs version_data
