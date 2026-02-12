import subprocess
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_cuda_and_get_metrics(hash_value: str):
    exe_path = os.path.join(
        BASE_DIR,
        "cuda_core",
        "src",
        "cuda_rainbow.exe"
    )

    result = subprocess.run(
        [exe_path, hash_value],
        capture_output=True,
        text=True
    )

    output = result.stdout

    time_match = re.search(r"CUDA_TIME_MS:(\d+\.?\d*)", output)
    time_ms = float(time_match.group(1)) if time_match else 0.0

    return output, time_ms
