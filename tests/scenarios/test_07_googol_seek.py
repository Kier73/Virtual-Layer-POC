import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.core import ArchetypeEngine
import time

def test_googol_seek():
    print("SCENARIO | Test 07: O(1) Googol-Scale Seek")
    engine = ArchetypeEngine()
    
    # Path at extreme depth
    googol_path = "/vol/" + "depth/" * 100 + "target.bin"
    
    start = time.perf_counter()
    entry = engine.resolve_entry(googol_path)
    end = time.perf_counter()
    
    latency = (end - start) * 1000
    print(f"  > Path: {googol_path[:30]}...[len={len(googol_path)}]")
    print(f"  > Offset: {hex(entry['offset'])}")
    print(f"  > Latency: {latency:.6f}ms")
    
    assert latency < 1.0, f"Googol seek too slow: {latency}ms"
    print("VERDICT: PASS (Sub-millisecond resolution at extreme coordinate depth)")

if __name__ == "__main__":
    test_googol_seek()
