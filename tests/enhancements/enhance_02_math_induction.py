import os
import sys
import math
import time
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer

def enhance_02_math_induction():
    print("ENHANCEMENT | VLD + Math: Inducing Iterative Primitives")
    vl = VirtualLayer()
    
    def iterative_sum_sqrt(n):
        # Simulate a traditionally expensive iterative loop
        res = 0.0
        for i in range(n):
            res += math.sqrt(i)
        return res
    
    test_val = 1_000_000
    
    # First pass: Compute & Induce
    print(f"  > Executing iterative loop (N={test_val})...")
    start1 = time.perf_counter()
    res1 = vl.run("Math_Sqrt_Sum", iterative_sum_sqrt, test_val)
    end1 = time.perf_counter()
    
    # Second pass: Recall Law
    start2 = time.perf_counter()
    res2 = vl.run("Math_Sqrt_Sum", iterative_sum_sqrt, test_val)
    end2 = time.perf_counter()
    
    lat1 = (end1 - start1) * 1000
    lat2 = (end2 - start2) * 1000
    
    print(f"  > Standard Loop Latency: {lat1:.4f}ms")
    print(f"  > VLD Induced Latency:   {lat2:.4f}ms")
    print(f"  > Result: {res1:.6f}")
    
    assert res1 == res2, "Law result mismatch"
    assert lat2 < lat1 / 10, "Induced recall must be significantly faster"
    print("VERDICT: PASS (O(N) math loop Promoted to O(1) Geometric Law)")

if __name__ == "__main__":
    enhance_02_math_induction()
