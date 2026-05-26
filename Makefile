.PHONY: all install uninstall build clean check

PREFIX     ?= /usr/local/bin
BIN_DIR     = bin
SRC_CORE    = src/core

# ────────────────────────────────────────────────
# Detect available toolchains
# ────────────────────────────────────────────────
HAS_GCC    := $(shell command -v gcc     2>/dev/null)
HAS_RUSTC  := $(shell command -v rustc   2>/dev/null)
HAS_KOTLINC:= $(shell command -v kotlinc 2>/dev/null)
HAS_JAVAC  := $(shell command -v javac   2>/dev/null)
HAS_NASM   := $(shell command -v nasm    2>/dev/null)

all: build

build: prep c_build rust_build kotlin_build java_build asm_build

prep:
	@mkdir -p $(BIN_DIR)

# ── C: fast port scanner ────────────────────────
c_build:
	@if [ -n "$(HAS_GCC)" ]; then \
	  echo "[CC]  Building sub-scan (C)..."; \
	  gcc -O2 -o $(BIN_DIR)/sub-scan $(SRC_CORE)/scanner.c \
	    && echo "      → bin/sub-scan OK"; \
	else echo "[SKIP] gcc not found — skipping sub-scan"; fi

# ── Rust: recon & crypto engine ─────────────────
rust_build:
	@if [ -n "$(HAS_RUSTC)" ]; then \
	  echo "[RS]  Building sub-recon (Rust)..."; \
	  rustc -O -o $(BIN_DIR)/sub-recon $(SRC_CORE)/recon.rs \
	    && echo "      → bin/sub-recon OK"; \
	else echo "[SKIP] rustc not found — skipping sub-recon"; fi

# ── Kotlin: threaded net utilities ──────────────
kotlin_build:
	@if [ -n "$(HAS_KOTLINC)" ]; then \
	  echo "[KT]  Building sub-net (Kotlin)..."; \
	  kotlinc $(SRC_CORE)/NetUtils.kt -include-runtime -d $(BIN_DIR)/sub-net.jar 2>/dev/null \
	    && echo "      → bin/sub-net.jar OK"; \
	else echo "[SKIP] kotlinc not found — skipping sub-net"; fi

# ── Java: OSINT tools ───────────────────────────
java_build:
	@if [ -n "$(HAS_JAVAC)" ]; then \
	  echo "[JV]  Building sub-osint (Java)..."; \
	  javac -d $(BIN_DIR) $(SRC_CORE)/OsintTools.java 2>/dev/null \
	    && echo "      → bin/OsintTools.class OK"; \
	else echo "[SKIP] javac not found — skipping sub-osint"; fi

# ── ASM: sysinfo native module ──────────────────
asm_build:
	@if [ -n "$(HAS_NASM)" ]; then \
	  echo "[ASM] Building sub-sysinfo (NASM)..."; \
	  nasm -f elf64 -o $(BIN_DIR)/sysinfo.o $(SRC_CORE)/sysinfo.asm \
	    && ld -o $(BIN_DIR)/sub-sysinfo $(BIN_DIR)/sysinfo.o \
	    && echo "      → bin/sub-sysinfo OK"; \
	else echo "[SKIP] nasm not found — skipping sub-sysinfo"; fi

# ── Install everything to PREFIX ────────────────
install: build
	@echo "[INSTALL] Installing to $(PREFIX)..."
	# Python master dispatcher
	cp src/sub.py $(PREFIX)/sub.py
	cp sub         $(PREFIX)/sub
	chmod +x $(PREFIX)/sub $(PREFIX)/sub.py
	# Native binaries (install only if built)
	@[ -f $(BIN_DIR)/sub-scan    ] && cp $(BIN_DIR)/sub-scan    $(PREFIX)/ && echo "  + sub-scan"    || true
	@[ -f $(BIN_DIR)/sub-recon   ] && cp $(BIN_DIR)/sub-recon   $(PREFIX)/ && echo "  + sub-recon"   || true
	@[ -f $(BIN_DIR)/sub-net.jar ] && cp $(BIN_DIR)/sub-net.jar $(PREFIX)/ && echo "  + sub-net.jar" || true
	@[ -f $(BIN_DIR)/sub-sysinfo ] && cp $(BIN_DIR)/sub-sysinfo $(PREFIX)/ && echo "  + sub-sysinfo" || true
	@echo "[INSTALL] Done. Run: sub help"

uninstall:
	@echo "[UNINSTALL] Removing sub tools..."
	rm -f $(PREFIX)/sub $(PREFIX)/sub.py
	rm -f $(PREFIX)/sub-scan $(PREFIX)/sub-recon
	rm -f $(PREFIX)/sub-net.jar $(PREFIX)/sub-sysinfo
	@echo "Done."

check:
	@echo "Toolchain availability:"
	@command -v gcc     && echo "  gcc     : found" || echo "  gcc     : MISSING"
	@command -v rustc   && echo "  rustc   : found" || echo "  rustc   : MISSING"
	@command -v kotlinc && echo "  kotlinc : found" || echo "  kotlinc : MISSING"
	@command -v javac   && echo "  javac   : found" || echo "  javac   : MISSING"
	@command -v nasm    && echo "  nasm    : found" || echo "  nasm    : MISSING"
	@command -v python3 && echo "  python3 : found" || echo "  python3 : MISSING"

clean:
	rm -rf $(BIN_DIR) *.deb
