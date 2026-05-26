# sub — Haxe Edition

**File:** `Sub.hx`

Haxe is a high-level, strictly typed language that compiles to **multiple targets**: JavaScript, Python, C++, Java, C#, PHP, Lua, HashLink, and Neko. This means a single `Sub.hx` source runs everywhere.

---

## Install Haxe

```bash
# Ubuntu/Debian
sudo apt install haxe

# Or via official installer
# https://haxe.org/download/
```

---

## Build & Run

### HashLink (native VM — fastest to build)
```bash
haxe build-hl.hxml
hl sub.hl banner
hl sub.hl whoami
```

### JavaScript
```bash
haxe build-js.hxml
node sub.js whoami
```

### Python
```bash
haxe build-py.hxml
python3 sub.py info
```

### C++ (native binary)
```bash
haxe build-cpp.hxml
./bin/Sub whoami
```

---

## Commands

| Command | Description |
|---|---|
| `banner` | Show ASCII banner |
| `whoami` | Author info |
| `info` | System info + detected compile target |

---

## Why Haxe?

Haxe is used in game dev (Heaps.io, HaxeFlixel, OpenFL), cross-platform tooling, and compiler research — all areas Subhobhai works in.
