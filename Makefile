# =============================================================
#  SUB — Multi-language Makefile
#  Compiles: C scanner, Rust recon, ASM sysinfo, Python dispatcher
# =============================================================

PREFIX   ?= /usr/local
BINDIR    = $(PREFIX)/bin
SRC       = src
CORE      = $(SRC)/core

# Compiler flags
CC        = gcc
CFLAGS    = -O2 -Wall -Wextra -o
RUSTC     = rustc
RFLAGS    = -O -o
NASM      = nasm
LD        = ld

# Output binaries
BIN_SCAN    = $(CORE)/sub-scan
BIN_RECON   = $(CORE)/sub-recon
BIN_SYSINFO = $(CORE)/sub-sysinfo
BIN_MAIN    = $(SRC)/sub.py

.PHONY: all build install uninstall clean build-deb

## Default target
all: build

## Build all binaries
build: build-c build-rust build-asm
	@echo "\n\033[92m[+] All binaries built successfully!\033[0m"
	@echo "\033[96m[*] Now run: sudo make install\033[0m\n"

## Build C scanner
build-c:
	@echo "\033[96m[*] Compiling C scanner...\033[0m"
	$(CC) $(CFLAGS) $(BIN_SCAN) $(CORE)/scanner.c
	@echo "\033[92m[+] sub-scan compiled.\033[0m"

## Build Rust recon
build-rust:
	@echo "\033[96m[*] Compiling Rust recon...\033[0m"
	$(RUSTC) $(RFLAGS) $(BIN_RECON) $(CORE)/recon.rs
	@echo "\033[92m[+] sub-recon compiled.\033[0m"

## Build Assembly sysinfo
build-asm:
	@echo "\033[96m[*] Assembling ASM sysinfo...\033[0m"
	$(NASM) -f elf64 $(CORE)/sysinfo.asm -o $(CORE)/sysinfo.o
	$(LD) -o $(BIN_SYSINFO) $(CORE)/sysinfo.o
	@rm -f $(CORE)/sysinfo.o
	@echo "\033[92m[+] sub-sysinfo assembled.\033[0m"

## Install all to /usr/local/bin
install: build
	@echo "\033[96m[*] Installing SUB binaries...\033[0m"
	install -Dm755 $(BIN_MAIN)    $(DESTDIR)$(BINDIR)/sub
	install -Dm755 $(BIN_SCAN)    $(DESTDIR)$(BINDIR)/sub-scan
	install -Dm755 $(BIN_RECON)   $(DESTDIR)$(BINDIR)/sub-recon
	install -Dm755 $(BIN_SYSINFO) $(DESTDIR)$(BINDIR)/sub-sysinfo
	@echo "\033[92m[+] SUB installed! Run: sub --help\033[0m\n"

## Uninstall
uninstall:
	rm -f $(DESTDIR)$(BINDIR)/sub
	rm -f $(DESTDIR)$(BINDIR)/sub-scan
	rm -f $(DESTDIR)$(BINDIR)/sub-recon
	rm -f $(DESTDIR)$(BINDIR)/sub-sysinfo
	@echo "\033[91m[-] SUB uninstalled.\033[0m"

## Clean build artifacts
clean:
	rm -f $(CORE)/sub-scan $(CORE)/sub-recon $(CORE)/sub-sysinfo $(CORE)/sysinfo.o
	rm -rf debian/.debhelper debian/sub debian/files *.deb *.buildinfo *.changes dist/
	@echo "\033[93m[*] Cleaned.\033[0m"

## Build .deb package
build-deb:
	@echo "\033[96m[*] Building .deb package...\033[0m"
	dpkg-buildpackage -us -uc -b
	mkdir -p dist && mv ../*.deb dist/ 2>/dev/null || true
	@echo "\033[92m[+] Done! Check dist/ for .deb\033[0m"
