import os
import sys
sys.path.append(os.getcwd())
import numpy as np
from vld_sdk.matrix import VMatrix
import math

def test_v_orthogonality():
    print("SCRUTINY | Test 01: V-Series Quasi-Orthogonality")
    seed = 0x1337
    vm = VMatrix(seed)
    
    # Extract two 'rows' by projecting one-hot vectors
    e0 = [1.0 if i == 0 else 0.0 for i in range(100)]
    e1 = [1.0 if i == 1 else 0.0 for i in range(100)]
    
    r1 = vm.project(e0, 1000)
    r2 = vm.project(e1, 1000)
    
    dot = sum(a * b for a, b in zip(r1, r2))
    norm1 = sum(a*a for a in r1)**0.5
    norm2 = sum(b*b for b in r2)**0.5
    
    similarity = abs(dot / (norm1 * norm2))
    print(f"  > Dot Product: {dot:.6f}")
    print(f"  > Cosine Similarity: {similarity:.6f}")
    
    # Orthogonality in high dimensions usually means similarity < 0.1
    assert similarity < 0.1, f"Cosine similarity too high: {similarity}"
    print("VERDICT: PASS (Spectral Projections are Quasi-Orthogonal)")

if __name__ == "__main__":
    test_v_orthogonality()
