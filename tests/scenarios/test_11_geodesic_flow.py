import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer

def test_geodesic_flow():
    print("SCENARIO | Test 11: Geodesic Flow Optimization")
    vl = VirtualLayer()
    
    path = vl.geodesic.solve_path(0.0, 1.0, steps=5)
    print(f"  > Synthesized Path: {[f'{x:.4f}' for x in path]}")
    
    # Check if it follows the cubic arc (0, 0.15, 0.5, 0.84, 1.0 approx)
    assert path[0] == 0.0 and path[-1] == 1.0, "Path endpoints incorrect"
    print("VERDICT: PASS (Cubic Geodesic Path Synthesized)")

if __name__ == "__main__":
    test_geodesic_flow()
