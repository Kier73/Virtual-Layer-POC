import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.matrix import XMatrix
import numpy as np

def test_x_isomorphism():
    print("SCRUTINY | Test 03: X-Series Descriptor Isomorphism")
    xm1 = XMatrix(10, 10, seed=0x111)
    xm2 = XMatrix(10, 10, seed=0x111) # Identical seed/structure
    
    desc1 = xm1.manifold.data
    desc2 = xm2.manifold.data
    
    # The descriptors should be holographically identical
    print(f"  > Descriptor 1 Signature: {desc1[:4]}...")
    print(f"  > Descriptor 2 Signature: {desc2[:4]}...")
    
    isomorphic = np.array_equal(desc1, desc2)
    print(f"  > Bit-Exact Isomorphism: {isomorphic}")
    
    assert isomorphic, "Tensors with same seed must be isomorphic"
    print("VERDICT: PASS (Structural Tensor Identity Detected)")

if __name__ == "__main__":
    test_x_isomorphism()
