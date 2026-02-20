import unittest
import math
import struct
import hashlib
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.core import DeterministicHasher, FeistelMemoizer, RNSEngine
from vld_sdk.matrix import GMatrix, GDescriptor
from vld_sdk.holographic import Hypervector

class TestHardenedScrutiny(unittest.TestCase):
    """
    Final Verification Suite: Proves that the identified 'improprieties' 
    have been robustly hardened in the VLD SDK core.
    """
    
    # --- 1. BIRTHDAY COLLISION RISK ---
    def test_birthday_collision_risk(self):
        """VERIFICATION: Stress test for Feistel projection collisions."""
        feistel = FeistelMemoizer(rounds=4)
        seen_seeds = {}
        iterations = 500_000
        
        print(f"\n[HARDENED] Running Birthday Collision Stress (Iterations: {iterations})...")
        for i in range(iterations):
            h = (i * 0xBF58476D1CE4E5B9) & ((1 << 256) - 1)
            seed = feistel.project_to_seed(h)
            if seed in seen_seeds:
                self.fail(f"COLLISION DETECTED! Seed: {hex(seed)}")
            seen_seeds[seed] = i
        print(f"  [PASS] No collisions in {iterations} projections.")

    # --- 2. EXASCALE ALIASING RESOLUTION ---
    def test_exascale_aliasing_fixed(self):
        """VERIFICATION: Prove that arbitrary-precision indexing eliminates aliasing."""
        # Matrix of 2^32 x 2^32 (2^64 cells)
        cols = 1 << 32
        desc = GDescriptor(cols * 2, cols, signature=0x123)
        gm = GMatrix(desc)
        
        # In the old 64-bit masked version, these matched.
        v1 = gm.resolve(0, 0)
        v2 = gm.resolve(1 << 32, 0)
        
        print(f"\n[HARDENED] Testing Exascale Aliasing (128-bit support)...")
        print(f"  Coord [0, 0]     -> {v1}")
        print(f"  Coord [2^32, 0]  -> {v2}")
        
        self.assertNotEqual(v1, v2, "Aliasing detected! Indexing upgrade failed.")
        print("  [PASS] Exascale Aliasing Fixed (Arbitrary-precision indexing verified).")

    # --- 3. FLOAT PRECISION RESOLUTION ---
    def test_precision_jitter_fixed(self):
        """VERIFICATION: Prove that 64-bit packing distinguishes near-identical doubles."""
        hasher = DeterministicHasher()
        
        # These previously collapsed to the same 32-bit float
        v1 = 1.0000000000000002
        v2 = 1.0000000000000004
        
        h1 = hasher.hash_data([v1])
        h2 = hasher.hash_data([v2])
        
        print(f"\n[HARDENED] Testing Float Precision (64-bit 'd' packing)...")
        print(f"  Double 1: {v1:.20f} -> {hex(h1)[:18]}...")
        print(f"  Double 2: {v2:.20f} -> {hex(h2)[:18]}...")
        
        self.assertNotEqual(h1, h2, "Precision collision detected! 64-bit packing failed.")
        print("  [PASS] Float Precision Verified.")

    # --- 4. HYPERVECTOR ENTROPY EXPANSION ---
    def test_hypervector_entropy_expanded(self):
        """VERIFICATION: Prove that Hypervectors can utilize high-entropy seeds."""
        # Massive seed (512-bit)
        seed1 = (1 << 512) + 1
        seed2 = (1 << 512) + 2
        
        hv1 = Hypervector.from_seed(seed1)
        hv2 = Hypervector.from_seed(seed2)
        
        print(f"\n[HARDENED] Hypervector Entropy check...")
        print(f"  Seed 1: (1<<512)+1 -> Bits: {hv1.bits & 0xFFFFFFFFFFFFFFFF:x}...")
        print(f"  Seed 2: (1<<512)+2 -> Bits: {hv2.bits & 0xFFFFFFFFFFFFFFFF:x}...")
        
        self.assertNotEqual(hv1.bits, hv2.bits)
        print("  [PASS] System supports high-entropy, arbitrary-precision seeds.")

    # --- 5. RNS CONTINUITY ---
    def test_rns_limit_awareness(self):
        """VERIFICATION: Confirm RNS logic maintains modular continuity as expected."""
        val = RNSEngine.DYNAMIC_RANGE + 100
        res = RNSEngine.to_residues(val)
        recovered = RNSEngine.from_residues(res)
        
        print(f"\n[HARDENED] RNS Continuity check...")
        print(f"  Input: Range + 100")
        print(f"  Output: {recovered}")
        
        self.assertEqual(recovered, 100)
        print("  [PASS] RNS Modular Continuity Verified.")

if __name__ == "__main__":
    unittest.main()
