# sub — CUDA Edition

**File:** `sub.cu`  
**Compile:** `nvcc sub.cu -o sub`  
**Requires:** NVIDIA GPU + CUDA Toolkit

## Commands

| Command | Description |
|---|---|
| `sub banner` | Show ASCII banner |
| `sub whoami` | Author info |
| `sub gpuinfo` | CUDA GPU details + live kernel launch demo |

## Build

```bash
# Install CUDA Toolkit (if not already)
# https://developer.nvidia.com/cuda-downloads

nvcc src/cuda/sub.cu -o sub
./sub gpuinfo
```

## No GPU? No Problem

The `gpuinfo` command detects if no CUDA GPU is present and falls back gracefully with a CPU-only message. `banner` and `whoami` always work regardless.

## Cross-compile for Jetson / Embedded ARM

```bash
nvcc -arch=sm_72 sub.cu -o sub-jetson  # Jetson Xavier
nvcc -arch=sm_87 sub.cu -o sub-orin    # Jetson Orin
```
