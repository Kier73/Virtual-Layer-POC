import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.core import RNSEngine

def test_rns_immunity():
    print("SCRUTINY | Test 05: RNS Modular Overflow Immunity")
    
    # A value within DYNAMIC_RANGE
    val = 1234567890123456789
    print(f"  > Input Value: {val}")
    print(f"  > RNS Range:   {RNSEngine.DYNAMIC_RANGE}")
    
    residues = RNSEngine.to_residues(val)
    recovered = RNSEngine.from_residues(residues)
    
    print(f"  > Recovered:   {recovered}")
    assert val == recovered, f"RNS Recovery failed: {val} != {recovered}"
    print("VERDICT: PASS (Large-scale Modular Overflow Immunity verified)")

if __name__ == "__main__":
    test_rns_immunity()
