/**
 * sub - The SUB Hacking & Info Tool (CUDA C++)
 * Author: Subhobhai (subhobhai943)
 * GitHub: https://github.com/subhobhai943
 * Compile: nvcc sub.cu -o sub
 * Run:     ./sub [banner|whoami|gpuinfo]
 *
 * Note: Falls back to CPU path if no CUDA GPU is present.
 */

#include <stdio.h>
#include <string.h>
#include <cuda_runtime.h>

#define RESET   "\033[0m"
#define GREEN   "\033[1;32m"
#define CYAN    "\033[1;36m"
#define YELLOW  "\033[1;33m"

const char* BANNER =
    "\n"
    "  +-+-+-+\n"
    "  |S|U|B|\n"
    "  +-+-+-+\n"
    "  by Subhobhai | github.com/subhobhai943\n"
    "  CUDA Edition\n\n";

// GPU kernel: each thread prints its own ID (demonstration)
__global__ void sub_gpu_hello(int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid < n) {
        printf("  [GPU Thread %3d] SUB is running on the GPU!\n", tid);
    }
}

void cmd_banner() {
    printf("%s", BANNER);
}

void cmd_whoami() {
    printf("%s", BANNER);
    printf(GREEN "  %-12s" RESET ": %s\n", "Name",      "Subhobhai Sarkar");
    printf(GREEN "  %-12s" RESET ": %s\n", "Alias",     "sub");
    printf(GREEN "  %-12s" RESET ": %s\n", "GitHub",    "https://github.com/subhobhai943");
    printf(GREEN "  %-12s" RESET ": %s\n", "Portfolio", "https://sub-portofolio.netlify.app");
    printf(GREEN "  %-12s" RESET ": %s\n", "Location",  "Durgapur, West Bengal, India");
    printf(GREEN "  %-12s" RESET ": %s\n", "Bio",       "PCMB student | Web, AI, C++/C# game dev");
    printf(GREEN "  %-12s" RESET ": %s\n", "Projects",  "AIOS, SUB lang, Discord bots, 3D web games");
    printf(GREEN "  %-12s" RESET ": %s\n", "Languages", "C, C++, Python, Rust, CUDA, Kotlin, Java, ASM");
    printf("\n");
}

void cmd_gpuinfo() {
    printf(CYAN "\n[*] CUDA GPU Information\n" RESET);
    int deviceCount = 0;
    cudaError_t err = cudaGetDeviceCount(&deviceCount);

    if (err != cudaSuccess || deviceCount == 0) {
        printf("  [!] No CUDA-capable GPU detected.\n");
        printf("  [i] Running in CPU-only mode.\n\n");
        return;
    }

    for (int i = 0; i < deviceCount; i++) {
        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, i);
        printf(YELLOW "  GPU %d:\n" RESET, i);
        printf("    Name           : %s\n",   prop.name);
        printf("    Compute Cap    : %d.%d\n", prop.major, prop.minor);
        printf("    Global Memory  : %.0f MB\n", (float)prop.totalGlobalMem / (1024*1024));
        printf("    SM Count       : %d\n",   prop.multiProcessorCount);
        printf("    Max Threads/SM : %d\n",   prop.maxThreadsPerMultiProcessor);
        printf("    Warp Size      : %d\n",   prop.warpSize);
        printf("    Clock Rate     : %.0f MHz\n", prop.clockRate / 1000.0f);
        printf("\n");
    }

    // Launch a small demo kernel
    printf(CYAN "[*] Launching GPU kernel (8 threads)...\n" RESET);
    sub_gpu_hello<<<1, 8>>>(8);
    cudaDeviceSynchronize();
    printf("\n");
}

void print_help() {
    printf("%s", BANNER);
    printf("Usage: sub <command>\n\n");
    printf("Commands:\n");
    printf("  banner    Show ASCII banner\n");
    printf("  whoami    Author info\n");
    printf("  gpuinfo   CUDA GPU details + kernel launch demo\n\n");
    printf("GitHub: https://github.com/subhobhai943\n\n");
}

int main(int argc, char* argv[]) {
    if (argc < 2) { print_help(); return 0; }

    if      (strcmp(argv[1], "banner")  == 0) cmd_banner();
    else if (strcmp(argv[1], "whoami")  == 0) cmd_whoami();
    else if (strcmp(argv[1], "gpuinfo") == 0) cmd_gpuinfo();
    else    { print_help(); return 1; }

    return 0;
}
