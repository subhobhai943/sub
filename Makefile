# =============================================================
#  SUB — Multi-language Makefile
#  Languages: Python · C · Rust · Assembly · Kotlin · Java
# =============================================================

PREFIX    ?= /usr/local
BINDIR     = $(PREFIX)/bin
SHAREDIR   = $(PREFIX)/share/sub
SRC        = src
CORE       = $(SRC)/core

CC         = gcc
CFLAGS     = -O2 -Wall -Wextra
RUSTC      = rustc
RFLAGS     = -O
NASM       = nasm
LD         = ld
KOTLNC     = kotlinc
JAVAC      = javac
JAR        = jar

.PHONY: all build install uninstall clean build-deb \
        build-c build-rust build-asm build-kotlin build-java

all: build

## Build all
build: build-c build-rust build-asm build-kotlin build-java
	@echo "\n\033[92m[+] All 5 binaries/JARs built!\033[0m"
	@echo "\033[96m[*] Run: sudo make install\033[0m\n"

## ── C
build-c:
	@echo "\033[96m[*] Compiling C scanner...\033[0m"
	$(CC) $(CFLAGS) -o $(CORE)/sub-scan $(CORE)/scanner.c
	@echo "\033[92m[+] sub-scan OK\033[0m"

## ── Rust
build-rust:
	@echo "\033[96m[*] Compiling Rust recon...\033[0m"
	$(RUSTC) $(RFLAGS) -o $(CORE)/sub-recon $(CORE)/recon.rs
	@echo "\033[92m[+] sub-recon OK\033[0m"

## ── Assembly
build-asm:
	@echo "\033[96m[*] Assembling x86-64 sysinfo...\033[0m"
	$(NASM) -f elf64 $(CORE)/sysinfo.asm -o $(CORE)/sysinfo.o
	$(LD) -o $(CORE)/sub-sysinfo $(CORE)/sysinfo.o
	@rm -f $(CORE)/sysinfo.o
	@echo "\033[92m[+] sub-sysinfo OK\033[0m"

## ── Kotlin → JAR
build-kotlin:
	@echo "\033[96m[*] Compiling Kotlin net module...\033[0m"
	$(KOTLINC) $(CORE)/NetUtils.kt -include-runtime -d $(CORE)/sub-net.jar 2>/dev/null
	@echo "\033[92m[+] sub-net.jar OK\033[0m"

## ── Java → JAR
build-java:
	@echo "\033[96m[*] Compiling Java OSINT module...\033[0m"
	$(JAVAC) -d $(CORE)/java_classes $(CORE)/OsintTools.java
	$(JAR) cfe $(CORE)/sub-osint.jar OsintTools -C $(CORE)/java_classes .
	@rm -rf $(CORE)/java_classes
	@echo "\033[92m[+] sub-osint.jar OK\033[0m"

## Install
install:
	@echo "\033[96m[*] Installing SUB...\033[0m"
	# Main CLI
	install -Dm755 $(SRC)/sub.py          $(DESTDIR)$(BINDIR)/sub
	# Compiled binaries
	install -Dm755 $(CORE)/sub-scan       $(DESTDIR)$(BINDIR)/sub-scan
	install -Dm755 $(CORE)/sub-recon      $(DESTDIR)$(BINDIR)/sub-recon
	install -Dm755 $(CORE)/sub-sysinfo    $(DESTDIR)$(BINDIR)/sub-sysinfo
	# JARs
	mkdir -p $(DESTDIR)$(SHAREDDIR)
	install -Dm644 $(CORE)/sub-net.jar    $(DESTDIR)$(SHAREDDIR)/sub-net.jar
	install -Dm644 $(CORE)/sub-osint.jar  $(DESTDIR)$(SHAREDDIR)/sub-osint.jar
	@echo "\033[92m[+] SUB v3.0.0 installed! Run: sub --help\033[0m\n"

## Uninstall
uninstall:
	rm -f  $(DESTDIR)$(BINDIR)/sub
	rm -f  $(DESTDIR)$(BINDIR)/sub-scan
	rm -f  $(DESTDIR)$(BINDIR)/sub-recon
	rm -f  $(DESTDIR)$(BINDIR)/sub-sysinfo
	rm -rf $(DESTDIR)$(SHAREDDIR)
	@echo "\033[91m[-] SUB uninstalled.\033[0m"

## Clean
clean:
	rm -f  $(CORE)/sub-scan $(CORE)/sub-recon $(CORE)/sub-sysinfo
	rm -f  $(CORE)/sub-net.jar $(CORE)/sub-osint.jar $(CORE)/sysinfo.o
	rm -rf $(CORE)/java_classes
	rm -rf debian/.debhelper debian/sub debian/files *.deb *.buildinfo *.changes dist/
	@echo "\033[93m[*] Cleaned.\033[0m"

## Build .deb
build-deb:
	dpkg-buildpackage -us -uc -b
	mkdir -p dist && mv ../*.deb dist/ 2>/dev/null || true
