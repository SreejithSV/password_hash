import numpy as np
from numba import cuda
import hashlib
import time

@cuda.jit
def gpu_dummy_kernel(data):
    idx = cuda.grid(1)
    if idx < data.size:
        data[idx] = data[idx] * 2
