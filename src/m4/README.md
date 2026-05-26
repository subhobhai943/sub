# sub — M4 Macro Edition

**File:** `sub.m4`  
**Run:** `m4 sub.m4`

M4 is a general-purpose macro processor used heavily in GNU Autotools (`configure.ac`, `Makefile.am`). This implementation uses M4 macros to define and expand author info and the SUB banner.

```bash
# Install m4 (usually pre-installed on Linux)
sudo apt install m4

# Run
m4 src/m4/sub.m4
```

### Extend it

You can use this as a template generator — pass it through `m4` before compiling other source files to inject author metadata automatically.
