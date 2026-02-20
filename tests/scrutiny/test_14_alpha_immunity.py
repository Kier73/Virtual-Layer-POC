import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.vm import mnCPU

def test_alpha_immunity():
    print("SCRUTINY | Test 14: Generative Processor (GP) Alpha-Renaming Immunity")
    cpu1 = mnCPU()
    cpu2 = mnCPU()
    
    # Prog 1: uses r0, r1
    cpu1.load('r0', 0.5)
    cpu1.load('r1', 0.8)
    
    # Prog 2: uses r30, r31 (Identical values, different indices)
    cpu2.load('r30', 0.5)
    cpu2.load('r31', 0.8)
    
    sig1 = cpu1.get_semantic_signature()
    sig2 = cpu2.get_semantic_signature()
    
    print(f"  > Signature A (r0, r1):   {hex(sig1)}")
    print(f"  > Signature B (r30, r31): {hex(sig2)}")
    
    assert sig1 == sig2, "Semantic signatures must be immune to alpha-renaming"
    print("VERDICT: PASS (GP Semantic Identity confirmed)")

if __name__ == "__main__":
    test_alpha_immunity()
