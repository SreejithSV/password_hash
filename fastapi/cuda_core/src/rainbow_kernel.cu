#include <string.h>
#include "config.h"

__global__ void lookupKernel(
    char* hash_db,
    char* text_db,
    int total,
    char* target_hash,
    char* output_text,
    int* found_flag
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx >= total) return;
    if (*found_flag) return;

    char* current_hash = hash_db + idx * HASH_LENGTH;

    bool match = true;
    for (int i = 0; i < HASH_LENGTH; i++) {
        if (current_hash[i] != target_hash[i]) {
            match = false;
            break;
        }
    }

    if (match) {
        if (atomicCAS(found_flag, 0, 1) == 0) {
            char* current_text = text_db + idx * MAX_TEXT_LEN;
            for (int i = 0; i < MAX_TEXT_LEN; i++) {
                output_text[i] = current_text[i];
                if (current_text[i] == '\0') break;
            }
        }
    }
}
