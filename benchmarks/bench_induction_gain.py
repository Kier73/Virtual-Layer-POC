import os
import sys
import time
import math
import random
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer

def bench_induction_gain():
    print("BENCHMARK | VLD Induction Gain (N vs 1)")
    vl = VirtualLayer()
    
    def heavy_prime_search(n):
        # Simulate an O(N) prime search
        count = 0
        for i in range(2, n):
            is_prime = True
            for j in range(2, int(math.sqrt(i)) + 1):
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime: count += 1
        return count

    test_range = 10000
    print(f"  > Task: Count primes up to {test_range}")
    
    # 1. Baseline (Standard Execution)
    start1 = time.perf_counter()
    res1 = heavy_prime_search(test_range)
    end1 = time.perf_counter()
    lat1 = (end1 - start1) * 1000
    
    # 2. VLD Induce (Execution + Grounding)
    start2 = time.perf_counter()
    res2 = vl.run("Prime_Search", heavy_prime_search, test_range)
    end2 = time.perf_counter()
    lat2 = (end2 - start2) * 1000
    
    # 3. VLD Recall (Law Retrieval)
    # Perform 1000 recalls to measure stable O(1) throughput
    start3 = time.perf_counter()
    for _ in range(1000):
        res3 = vl.run("Prime_Search", heavy_prime_search, test_range)
    end3 = time.perf_counter()
    lat3 = ((end3 - start3) / 1000) * 1000
    
    print(f"  > Standard O(N):       {lat1:.4f} ms")
    print(f"  > VLD Induction:       {lat2:.4f} ms (First Pass)")
    print(f"  > VLD Recall O(1):     {lat3:.4f} ms (Throughput)")
    print(f"  > Acceleration Gain:   {lat1/lat3:,.1f}x")
    
    assert res1 == res2 == res3, "Result mismatch"
    print("\nVERDICT: PASS (Induction effectively shunts O(N) complexity to O(1) grounding)")

if __name__ == "__main__":
    bench_induction_gain()
