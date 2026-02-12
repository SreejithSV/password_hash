#ifndef GPU_CHECK_H
#define GPU_CHECK_H

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

inline void enforceCUDA() {
    int deviceCount = 0;
    cudaGetDeviceCount(&deviceCount);

    if (deviceCount == 0) {
        printf("====================================\n");
        printf("ERROR: NVIDIA CUDA GPU REQUIRED\n");
        printf("This application cannot run on CPU\n");
        printf("====================================\n");
        exit(EXIT_FAILURE);
    }
}

#endif
