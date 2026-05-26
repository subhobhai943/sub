# sub — Assembly Implementations

Two native Assembly editions of `sub` with zero runtime dependencies.

---

## x86-64 (NASM)

**File:** `x86_64/sub.asm`  
**Target:** Linux x86-64 — Intel/AMD desktops, servers, WSL2

```bash
# Install NASM
sudo apt install nasm

# Assemble & link
nasm -f elf64 src/asm/x86_64/sub.asm -o sub.o
ld sub.o -o sub

# Run
./sub banner
./sub whoami
```

---

## AArch64 (GAS)

**File:** `aarch64/sub.s`  
**Target:** Linux AArch64 — Raspberry Pi 4/5, ARM servers, Android (Termux), Apple M-series Linux VM

```bash
# Assemble & link (on ARM64 Linux / Termux)
as src/asm/aarch64/sub.s -o sub.o
ld sub.o -o sub

# Run
./sub banner
./sub whoami
```

### Cross-compile from x86-64

```bash
sudo apt install binutils-aarch64-linux-gnu
aarch64-linux-gnu-as sub.s -o sub.o
aarch64-linux-gnu-ld sub.o -o sub-aarch64
```

---

## Commands (both editions)

| Command | Description |
|---|---|
| `sub banner` | Show ASCII banner |
| `sub whoami` | Author info |

> Full feature set (scan, ports, whois, update) lives in the Python edition: `src/python/sub.py`
