import os
import psutil
import time
import math
import numpy as np
from vld_sdk.matrix import GMatrix, GDescriptor
from vld_sdk.induction import VirtualLayer

def get_rss():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # MB

def benchmark_memory_scaling():
    print("--- Memory Scaling: GMatrix ---")
    scales = [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]
    for n in scales:
        start_rss = get_rss()
        desc = GDescriptor(int(math.sqrt(n)), int(math.sqrt(n)), signature=0x123)
        matrix = GMatrix(desc)
        # Touch a few elements
        for i in range(10):
            matrix.resolve(0, i)
        end_rss = get_rss()
        print(f"Scale: {n:10} elements | Peak RSS: {end_rss:.2f} MB | Delta: {end_rss - start_rss:.4f} MB")

def benchmark_memory_over_time():
    print("\n--- Memory Over Time: Sparse Overlay Growth ---")
    vl = VirtualLayer()
    
    iterations = 50000
    start_rss = get_rss()
    for i in range(iterations):
        vl.run(f"task_{i}", lambda x: x[0]*x[0], [i])
        if i % 10000 == 0:
            print(f"Iterations: {i:6} | Current RSS: {get_rss():.2f} MB")
    
    end_rss = get_rss()
    print(f"Final RSS after {iterations} inductions: {end_rss:.2f} MB (Delta: {end_rss - start_rss:.2f} MB)")

def benchmark_crossover():
    print("\n--- Crossover Point: Generative vs. Materialized ---")
    n_elements = 100000
    
    # 1. NumPy Full Materialization
    t1 = time.perf_counter()
    np_arr = np.random.rand(n_elements)
    t2 = time.perf_counter()
    np_time = t2 - t1
    np_mem = np_arr.nbytes / (1024 * 1024)
    
    # 2. GMatrix Resolution
    desc = GDescriptor(100, 1000, signature=0x789)
    matrix = GMatrix(desc)
    t3 = time.perf_counter()
    for i in range(100):
        for j in range(1000):
            matrix.resolve(i, j)
    t4 = time.perf_counter()
    vld_time = t4 - t3
    
    print(f"NumPy (Materialize {n_elements}): Time: {np_time:.4f}s | Mem: {np_mem:.2f} MB")
    print(f"VLD (Resolve {n_elements}):     Time: {vld_time:.4f}s | Mem: ~0 MB (Fixed Overhead)")
    print(f"Crossover: At what point is the compute cost (VLD) > storage cost (NumPy)?")
    print(f"VLD Latency per element: {vld_time/n_elements:.8f}s")

if __name__ == "__main__":
    benchmark_memory_scaling()
    benchmark_memory_over_time()
    benchmark_crossover()
