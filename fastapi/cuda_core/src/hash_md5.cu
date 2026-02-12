#include <stdint.h>

__device__ void simple_hash(const char* input, uint32_t* out) {
    uint32_t hash = 5381;
    for (int i = 0; i < 4; i++) {
        hash = ((hash << 5) + hash) + input[i];
    }
    *out = hash;
}
