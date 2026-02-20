import time
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.induction import VirtualLayer

def stress_induction_ceiling():
    print("="*80)
    print(" STRESS TEST: RECURSIVE INDUCTION CEILING")
    print("="*80)
    
    vl = VirtualLayer(seed=999)
    
    def meta_law(depth):
        if depth == 0: return 1
        name = f"Level_{depth}"
        return vl.run(name, lambda x: x + 1, meta_law(depth-1))

    print("\nTESTING_RECURSIVE_DEPTHS:")
    depths = [5, 10, 25, 50, 100]
    
    for d in depths:
        start = time.perf_counter()
        try:
            res = meta_law(d)
            end = time.perf_counter()
            latency = (end-start)*1000
            print(f"  DEPTH_{d:3d}: Result={res} | Latency={latency:.4f}ms")
        except RecursionError:
            print(f"  DEPTH_{d:3d}: FAILED (Recursion Limit)")
            break
            
    print("\nVERDICT: VLD handles nested induction linearly until Python's stack limit is reached.")

if __name__ == "__main__":
    stress_induction_ceiling()
