import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.vm import ResonanceGuard
import math

def test_resonance():
    print("SCRUTINY | Test 17: Proximity Resonance (Manifold Recall)")
    guard = ResonanceGuard(threshold=0.9)
    
    # High resonance: very close to integer alignment
    sig_high = 100.01 
    # Low resonance: far from integer alignment
    sig_low = 100.5 
    
    res_high = guard.verify(sig_high)
    res_low = guard.verify(sig_low)
    
    print(f"  > Sig 100.01 Resonance: {res_high}")
    print(f"  > Sig 100.50 Resonance: {res_low}")
    
    assert res_high == True and res_low == False, "Resonance verify logic failed"
    print("VERDICT: PASS (Manifold Proximity Resonance confirmed)")

if __name__ == "__main__":
    test_resonance()
