import time
import numpy as np
import math
from vld_sdk.matrix import GMatrix, GDescriptor
from vld_sdk.induction import VirtualLayer

def profile_latency_scaling():
    print("--- Latency Scaling: O(1) Verification ---")
    scales = [10**4, 10**6, 10**8, 10**10, 10**12]
    for n in scales:
        dim = int(math.sqrt(n))
        desc = GDescriptor(dim, dim, signature=0x123)
        matrix = GMatrix(desc)
        coords = [(np.random.randint(0, dim), np.random.randint(0, dim)) for _ in range(1000)]
        t1 = time.perf_counter()
        for r, c in coords:
            matrix.resolve(r, c)
        t2 = time.perf_counter()
        avg_lat = (t2 - t1) / 1000
        print(f"Matrix Scale: 10^{int(math.log10(n)):2} | Avg Latency: {avg_lat*1000000:.2f} us")

def profile_tail_latency():
    print("\n--- Tail Latency (p99/p999) ---")
    desc = GDescriptor(1000, 1000, signature=0x999)
    matrix = GMatrix(desc)
    latencies = []
    for _ in range(10000):
        r, c = np.random.randint(0, 1000), np.random.randint(0, 1000)
        t1 = time.perf_counter()
        matrix.resolve(r, c)
        t2 = time.perf_counter()
        latencies.append(t2 - t1)
    latencies = np.array(latencies) * 1000000 # us
    print(f"Mean: {np.mean(latencies):.2f} us")
    print(f"p50:  {np.percentile(latencies, 50):.2f} us")
    print(f"p99:  {np.percentile(latencies, 99):.2f} us")
    print(f"p99.9:{np.percentile(latencies, 99.9):.2f} us")

def profile_induction_scaling():
    print("\n--- Induction: Warm vs Cold Scaling ---")
    vl = VirtualLayer()
    def complex_fn(inputs):
        n = inputs[0]
        count = 0
        for i in range(2, n):
            is_prime = True
            for j in range(2, int(math.sqrt(i)) + 1):
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime: count += 1
        return count
    test_input = 2000
    t1 = time.perf_counter()
    res_cold = vl.run("PrimeSearch", complex_fn, [test_input])
    t2 = time.perf_counter()
    cold_time = t2 - t1
    t3 = time.perf_counter()
    res_warm = vl.run("PrimeSearch", complex_fn, [test_input])
    t4 = time.perf_counter()
    warm_time = t4 - t3
    print(f"Cold Time (Grounding): {cold_time:.4f}s")
    print(f"Warm Time (Shunted):   {warm_time:.6f}s")
    print(f"Induction Speedup:    {cold_time/warm_time:.2f}x")

if __name__ == "__main__":
    profile_latency_scaling()
    profile_tail_latency()
    profile_induction_scaling()
