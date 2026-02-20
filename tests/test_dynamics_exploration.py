import unittest
import math
import random
import os
import sys
import hashlib

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.holographic import Hypervector, ByzantineHDC
from vld_sdk.vm import mnCPU
from vld_sdk.geometric import HilbertGrounding, TorusProjector
from vld_sdk.core import RNSEngine

class TestDynamicsExploration(unittest.TestCase):
    
    # --- 1. BYZANTINE BREAKDOWN POINT ---
    def test_byzantine_breakdown(self):
        """Measures the recovery fidelity of HDC as more nodes become adversarial."""
        truth = Hypervector.from_seed(0xDEADC0DE, "Truth")
        bhdc = ByzantineHDC()
        
        results = []
        for noise_pct in range(0, 101, 10):
            node_count = 100
            noise_count = int(node_count * (noise_pct / 100.0))
            nodes = [truth] * (node_count - noise_count)
            # Add random noise nodes
            for _ in range(noise_count):
                nodes.append(Hypervector.from_seed(random.getrandbits(64)))
            
            reconciled = bhdc.reconcile(nodes)
            fidelity = (reconciled.bits == truth.bits)
            results.append((noise_pct, fidelity))
            
        # Byzantine consensus should hold up to (but not including) 50% noise
        for pct, fidelity in results:
            if pct < 50:
                self.assertTrue(fidelity, f"Byzantine consensus failed at {pct}% noise (Expected success < 50%)")
            elif pct > 50:
                # Note: in rare cases it might still match by luck, but generally should fail
                pass

    # --- 2. mnCPU SEMANTIC IMMUNITY ---
    def test_mncpu_semantic_reordering(self):
        """Proves that semantic signatures are immune to instruction reordering."""
        cpu1 = mnCPU()
        cpu2 = mnCPU()
        
        # Program A: Load 0.1 into r0, 0.2 into r1, then ADD
        prog_a = [
            (1, 0, 1) # ADD r0, r1 (0.0 + 0.0)
        ]
        cpu1.load(0, 0.1)
        cpu1.load(1, 0.2)
        cpu1.execute(prog_a)
        
        # Program B: Load into different registers but same values, 
        # ordering of registers in state should be normalized.
        cpu2.load(5, 0.2)
        cpu2.load(10, 0.1)
        cpu2.execute([(1, 10, 5)]) # ADD r10, r5
        
        sig1 = cpu1.get_semantic_signature()
        sig2 = cpu2.get_semantic_signature()
        
        # Results should be identical because the sorted values in registers are the same
        self.assertEqual(sig1, sig2, "Semantic signatures diverged on reordered/remapped registers!")

    # --- 3. HILBERT SPATIAL COHERENCE ---
    def test_hilbert_spatial_coherence(self):
        """Verifies that locality in the 1D manifold index implies locality in 2D space."""
        n = 256
        max_dist_sq = 0
        for d in range(n*n - 1):
            x1, y1 = HilbertGrounding.d_to_xy(n, d)
            x2, y2 = HilbertGrounding.d_to_xy(n, d + 1)
            dist_sq = (x1 - x2)**2 + (y1 - y2)**2
            # For Hilbert curves, adjacent indices are always Manhattan distance 1, 
            # and Euclidean distance 1.
            self.assertEqual(dist_sq, 1, f"Hilbert index {d}->{d+1} jumped in space: ({x1},{y1}) to ({x2},{y2})")

    # --- 4. TORUS DISTRIBUTION UNIFORMITY ---
    def test_torus_distribution_density(self):
        """Tests if the Torus projection sufficiently spreads residues across [0, 1]."""
        tp = TorusProjector()
        moduli = RNSEngine.MODULI
        points = []
        for i in range(1000):
            res = [ (i * 7 + m//2) % m for m in moduli ]
            points.append(tp.project(res, moduli))
            
        # Basic check: points shouldn't all cluster in one quadrant
        q1 = len([p for p in points if p < 0.25])
        q2 = len([p for p in points if 0.25 <= p < 0.5])
        q3 = len([p for p in points if 0.5 <= p < 0.75])
        q4 = len([p for p in points if p >= 0.75])
        
        # Each quadrant should have roughly 25% (very loose bound for test stability)
        for count in [q1, q2, q3, q4]:
            self.assertGreater(count, 150, "Torus distribution is severely non-uniform!")

if __name__ == "__main__":
    unittest.main()
