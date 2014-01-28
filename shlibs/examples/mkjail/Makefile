CHROOT_DARWIN=chroot -u nobody -g nobody
CHROOT_LINUX=chroot --userspec 65543:65534

PLATFORM=$(shell python -c "import platform; print platform.platform().split('-')[0]")
ifeq ($(PLATFORM),Darwin)
	CHROOT=$(CHROOT_DARWIN)
else
	CHROOT=$(CHROOT_LINUX)
endif

.PHONY: test clean

test: alcatraz
	sudo env - PATH="$$PATH" $(CHROOT) alcatraz bin/sh

alcatraz:
	sudo ./mkjail.py alcatraz /bin/* /sbin/* /usr/bin/* /usr/sbin/* /usr/local/bin/* /usr/local/sbin/*

clean:
	sudo rm -r alcatraz ; true
