import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer
import math
import time

def test_shunting():
    print("SCENARIO | Test 12: Algorithmic Shunting (Factorial O(N!))")
    vl = VirtualLayer()
    
    def slow_factorial(n):
        # Simulate O(N!) by redundant work
        res = 1
        for i in range(1, 10): # Keep it small for test speed
            res *= i
        time.sleep(0.01) # Simulate iterative delay
        return res
    
    # Pass 1: Slow
    start1 = time.perf_counter()
    vl.run("Factorial_Law", slow_factorial, 100)
    end1 = time.perf_counter()
    
    # Pass 2: Shunted
    start2 = time.perf_counter()
    vl.run("Factorial_Law", slow_factorial, 100)
    end2 = time.perf_counter()
    
    lat1 = (end1 - start1) * 1000
    lat2 = (end2 - start2) * 1000
    print(f"  > Baseline Latency: {lat1:.4f}ms")
    print(f"  > Shunted Latency:  {lat2:.4f}ms")
    
    assert lat2 < lat1 / 2, "Shunting failed to provide significant speedup"
    print("VERDICT: PASS (Algorithmic loop shunted to O(1) recall)")

if __name__ == "__main__":
    test_shunting()
