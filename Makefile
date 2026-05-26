.PHONY: all build install uninstall clean check

PREFIX   ?= /usr/local/bin
BIN      := bin
SC       := src/core
SJ       := src/java
SK       := src/kotlin
SH       := src/haxe
SCU      := src/cuda
SAX      := src/asm/x86_64
SAA      := src/asm/aarch64

# ── Detect toolchains ────────────────────────────────────────────────
HAS_GCC    := $(shell command -v gcc      2>/dev/null)
HAS_RUSTC  := $(shell command -v rustc    2>/dev/null)
HAS_KOTLINC:= $(shell command -v kotlinc  2>/dev/null)
HAS_JAVAC  := $(shell command -v javac    2>/dev/null)
HAS_HAXE   := $(shell command -v haxe     2>/dev/null)
HAS_NVCC   := $(shell command -v nvcc     2>/dev/null)
HAS_NASM   := $(shell command -v nasm     2>/dev/null)
HAS_AS     := $(shell command -v as       2>/dev/null)
HAS_M4     := $(shell command -v m4       2>/dev/null)
ARCH       := $(shell uname -m)

all: build

build: prep c_build rust_build kotlin_core_build kotlin_build java_core_build java_build haxe_build cuda_build asm_build m4_build

prep:
	@mkdir -p $(BIN)

# ── C ── scanner.c → bin/sub-scan ────────────────────────────────────
c_build:
	@if [ -n "$(HAS_GCC)" ]; then \
	  echo "[CC]  scanner.c → bin/sub-scan"; \
	  gcc -O2 -o $(BIN)/sub-scan $(SC)/scanner.c && echo "      OK"; \
	else echo "[SKIP] gcc missing — sub-scan"; fi

# ── Rust ── recon.rs → bin/sub-recon ─────────────────────────────────
rust_build:
	@if [ -n "$(HAS_RUSTC)" ]; then \
	  echo "[RS]  recon.rs → bin/sub-recon"; \
	  rustc -O -o $(BIN)/sub-recon $(SC)/recon.rs && echo "      OK"; \
	else echo "[SKIP] rustc missing — sub-recon"; fi

# ── Kotlin (core) ── NetUtils.kt → bin/sub-net.jar ───────────────────
kotlin_core_build:
	@if [ -n "$(HAS_KOTLINC)" ]; then \
	  echo "[KT]  NetUtils.kt → bin/sub-net.jar"; \
	  kotlinc $(SC)/NetUtils.kt -include-runtime -d $(BIN)/sub-net.jar 2>/dev/null && echo "      OK"; \
	else echo "[SKIP] kotlinc missing — sub-net"; fi

# ── Kotlin (standalone) ── Sub.kt → bin/sub-kt.jar ───────────────────
kotlin_build:
	@if [ -n "$(HAS_KOTLINC)" ]; then \
	  echo "[KT]  Sub.kt → bin/sub-kt.jar"; \
	  kotlinc $(SK)/Sub.kt -include-runtime -d $(BIN)/sub-kt.jar 2>/dev/null && echo "      OK"; \
	else echo "[SKIP] kotlinc missing — sub-kt"; fi

# ── Java (core) ── OsintTools.java → bin/ ────────────────────────────
java_core_build:
	@if [ -n "$(HAS_JAVAC)" ]; then \
	  echo "[JV]  OsintTools.java → bin/OsintTools.class"; \
	  javac -d $(BIN) $(SC)/OsintTools.java 2>/dev/null && echo "      OK"; \
	else echo "[SKIP] javac missing — OsintTools"; fi

# ── Java (standalone) ── Sub.java → bin/Sub.class ────────────────────
java_build:
	@if [ -n "$(HAS_JAVAC)" ]; then \
	  echo "[JV]  Sub.java → bin/Sub.class"; \
	  javac -d $(BIN) $(SJ)/Sub.java 2>/dev/null && echo "      OK"; \
	else echo "[SKIP] javac missing — Sub.java"; fi

# ── Haxe ── Sub.hx → bin/sub-haxe (C++ target) ──────────────────────
haxe_build:
	@if [ -n "$(HAS_HAXE)" ] && [ -n "$(HAS_GCC)" ]; then \
	  echo "[HX]  Sub.hx → bin/sub-haxe (cpp)"; \
	  haxe $(SH)/build-cpp.hxml 2>/dev/null && echo "      OK"; \
	else echo "[SKIP] haxe/gcc missing — sub-haxe"; fi

# ── CUDA ── sub.cu → bin/sub-cuda ────────────────────────────────────
cuda_build:
	@if [ -n "$(HAS_NVCC)" ]; then \
	  echo "[CU]  sub.cu → bin/sub-cuda"; \
	  nvcc -O2 -o $(BIN)/sub-cuda $(SCU)/sub.cu && echo "      OK"; \
	else echo "[SKIP] nvcc missing — sub-cuda"; fi

# ── ASM ── arch-aware: x86_64 (NASM) or aarch64 (GAS) ───────────────
asm_build:
	@if [ "$(ARCH)" = "x86_64" ] && [ -n "$(HAS_NASM)" ]; then \
	  echo "[ASM] sub.asm (x86_64 NASM) → bin/sub-asm"; \
	  nasm -f elf64 -o $(BIN)/sub-asm.o $(SAX)/sub.asm \
	    && ld -o $(BIN)/sub-asm $(BIN)/sub-asm.o && echo "      OK"; \
	elif [ "$(ARCH)" = "aarch64" ] && [ -n "$(HAS_AS)" ]; then \
	  echo "[ASM] sub.s (aarch64 GAS) → bin/sub-asm"; \
	  as -o $(BIN)/sub-asm.o $(SAA)/sub.s \
	    && ld -o $(BIN)/sub-asm $(BIN)/sub-asm.o && echo "      OK"; \
	else echo "[SKIP] nasm/as missing or unsupported arch — sub-asm"; fi
	@if [ -n "$(HAS_NASM)" ]; then \
	  echo "[ASM] sysinfo.asm → bin/sub-sysinfo"; \
	  nasm -f elf64 -o $(BIN)/sysinfo.o $(SC)/sysinfo.asm \
	    && ld -o $(BIN)/sub-sysinfo $(BIN)/sysinfo.o && echo "      OK" || true; \
	fi

# ── M4 ── sub.m4 → bin/sub-whoami.txt (pre-rendered) ────────────────
m4_build:
	@if [ -n "$(HAS_M4)" ]; then \
	  echo "[M4]  sub.m4 → bin/sub-whoami.txt"; \
	  m4 src/m4/sub.m4 > $(BIN)/sub-whoami.txt && echo "      OK"; \
	else echo "[SKIP] m4 missing — sub-whoami.txt"; fi

# ── Install ───────────────────────────────────────────────────────────
install: build
	@echo "[INSTALL] → $(PREFIX)"
	cp src/sub.py  $(PREFIX)/sub.py
	cp sub         $(PREFIX)/sub
	chmod +x $(PREFIX)/sub $(PREFIX)/sub.py
	@for b in sub-scan sub-recon sub-haxe sub-cuda sub-asm sub-sysinfo; do \
	  [ -x $(BIN)/$$b ] && cp $(BIN)/$$b $(PREFIX)/$$b && echo "  + $$b" || true; \
	done
	@for j in sub-net.jar sub-kt.jar; do \
	  [ -f $(BIN)/$$j ] && cp $(BIN)/$$j $(PREFIX)/$$j && echo "  + $$j" || true; \
	done
	@[ -d $(BIN)/Sub ] && cp -r $(BIN)/Sub $(PREFIX)/sub-haxe-bin || true
	@cp -f $(BIN)/*.class $(PREFIX)/ 2>/dev/null && echo "  + Java classes" || true
	@[ -f $(BIN)/sub-whoami.txt ] && cp $(BIN)/sub-whoami.txt $(PREFIX)/ || true
	@echo "[INSTALL] Done — run: sub help"

uninstall:
	@echo "[UNINSTALL] Removing sub..."
	rm -f $(PREFIX)/sub $(PREFIX)/sub.py
	rm -f $(PREFIX)/sub-scan $(PREFIX)/sub-recon
	rm -f $(PREFIX)/sub-net.jar $(PREFIX)/sub-kt.jar
	rm -f $(PREFIX)/sub-haxe $(PREFIX)/sub-cuda
	rm -f $(PREFIX)/sub-asm $(PREFIX)/sub-sysinfo
	rm -f $(PREFIX)/sub-whoami.txt
	rm -f $(PREFIX)/*.class
	@echo "Done."

check:
	@echo "Toolchain Status:"
	@for t in gcc rustc kotlinc javac haxe nvcc nasm as m4 python3; do \
	  command -v $$t >/dev/null 2>&1 \
	    && printf "  %-10s : \033[92mfound\033[0m\n" $$t \
	    || printf "  %-10s : \033[91mmissing\033[0m\n" $$t; \
	done
	@echo
	@echo "Built binaries in ./bin/:"
	@for b in sub-scan sub-recon sub-net.jar sub-kt.jar sub-haxe sub-cuda sub-asm sub-sysinfo sub-whoami.txt; do \
	  [ -e $(BIN)/$$b ] \
	    && printf "  %-20s : \033[92mbuilt\033[0m\n" $$b \
	    || printf "  %-20s : \033[91mnot built\033[0m\n" $$b; \
	done

clean:
	rm -rf $(BIN) *.deb
