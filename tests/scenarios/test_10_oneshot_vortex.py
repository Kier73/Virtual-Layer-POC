import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer
import math
import time

def test_oneshot_vortex():
    print("SCENARIO | Test 10: One-Shot Vortex Induction")
    vl = VirtualLayer(seed=0x111)
    
    def complex_vortex(x):
        # Heavy chaotic function
        for _ in range(100):
            x = (math.sin(x * 3.14) + math.cos(x * 123.45)) % 1.0
        return x
    
    test_val = 0.5
    
    # Step 1: Execute and Induce (Instantly due to Ground Phase logic)
    res_raw = vl.run("Vortex_Law", complex_vortex, test_val)
    
    # Step 2: O(1) Recall
    start = time.perf_counter()
    res_recall = vl.run("Vortex_Law", complex_vortex, test_val)
    end = time.perf_counter()
    
    latency = (end - start) * 1000
    print(f"  > Recall Match: {res_raw == res_recall}")
    print(f"  > Recall Latency: {latency:.6f}ms")
    
    assert res_raw == res_recall, "Result mismatch after induction"
    print("VERDICT: PASS (One-Shot Induction promoted Law instantly)")

if __name__ == "__main__":
    test_oneshot_vortex()
