# SUB Makefile
PREFIX ?= /usr/local
BINDIR  = $(PREFIX)/bin

install:
	install -Dm755 src/sub.py $(DESTDIR)$(BINDIR)/sub
	chmod +x $(DESTDIR)$(BINDIR)/sub

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/sub

build-deb:
	@echo "[*] Building .deb package..."
	dpkg-buildpackage -us -uc -b
	@echo "[+] Done! .deb is in the parent directory."

clean:
	rm -rf debian/.debhelper debian/sub debian/files *.deb *.buildinfo *.changes

.PHONY: install uninstall build-deb clean
