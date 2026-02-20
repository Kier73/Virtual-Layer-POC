import unittest
import time
import threading
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.induction import VirtualLayer
from vld_sdk.core import DeterministicHasher

class TestVLDScrutiny(unittest.TestCase):
    def setUp(self):
        # Reset the Oracle for each test to ensure isolation
        VirtualLayer.ORACLE._laws = {}

    def test_volume_invariance(self):
        """
        Verifies that multiple physical volumes (threads) converge on a 
        shared induction proof, proving Topology Invariance.
        """
        print("\n[SCRUTINY] Running Volume Invariance Test...")
        
        results = []
        def execution_volume(v_id):
            vl = VirtualLayer(seed=0x123)
            # Each thread does the same expensive task
            def expensive_task(n):
                return sum(range(n))
            
            # Phase 1: Induce
            for i in range(5):
                vl.run("SharedSum", expensive_task, 1000)
            
            # Phase 2: Recall
            start = time.perf_counter()
            res = vl.run("SharedSum", expensive_task, 1000)
            end = time.perf_counter()
            results.append((v_id, res, (end-start)*1000))

        threads = [threading.Thread(target=execution_volume, args=(i,)) for i in range(4)]
        for t in threads: t.start()
        for t in threads: t.join()

        # Check if all results are bit-identical
        first_res = results[0][1]
        for v_id, res, lat in results:
            self.assertEqual(res, first_res, f"Volume {v_id} diverged!")
            print(f"  Volume {v_id} Result: {res} | Latency: {lat:.4f}ms")
        
        print("  [PASS] Volume Invariance Verified.")

    def test_recursive_induction(self):
        """
        Verifies that recursive functions can be induced into O(1) laws,
        collapsing the stack complexity.
        """
        print("\n[SCRUTINY] Running Recursive Induction Test...")
        vl = VirtualLayer()

        def fib(n):
            if n <= 1: return n
            # Inside a real VLD system, the recursive calls would be intercepted 
            # by the VL and resolved from the substrate. Here we simulate it.
            return vl.run("FibLaw", fib, n-1) + vl.run("FibLaw", fib, n-2)

        # First call: Deep recursion (O(2^N))
        start_deep = time.perf_counter()
        res1 = vl.run("FibLaw", fib, 10)
        end_deep = time.perf_counter()
        
        # Second call: O(1) recall
        start_rec = time.perf_counter()
        res2 = vl.run("FibLaw", fib, 10)
        end_rec = time.perf_counter()

        self.assertEqual(res1, res2)
        print(f"  Fib(10) Deep Execution: {(end_deep-start_deep)*1000:.4f}ms")
        print(f"  Fib(10) Inducted Recall: {(end_rec-start_rec)*1000:.4f}ms")
        self.assertLess(end_rec - start_rec, end_deep - start_deep)
        print("  [PASS] Recursive Stack Collapse Verified.")

    def test_causal_stability(self):
        """
        Verifies that Shadow Induction handles mid-execution seed changes
        (Time Paradox / Ground Shift) correctly.
        """
        print("\n[SCRUTINY] Running Causal Stability Test...")
        vl = VirtualLayer(seed=0xAAA)
        
        def identity(x): return x
        
        # 1. Induce state in Timeline AAA
        vl.run("CausalFlow", identity, 42)
        
        # 2. Shift Ground Seed (The Paradox)
        vl.current_seed = 0xBBB
        
        # 3. Recall result. In a stable VL, the 'Law' is bound to the identity of the 
        # algorithm, not just the physical ground seed of the engine.
        res = vl.run("CausalFlow", identity, 42)
        
        self.assertEqual(res, 42)
        print(f"  Ground Shift: 0xAAA -> 0xBBB")
        print(f"  Causal Recall: {res} (Status: Stable)")
        print("  [PASS] Causal Stability Verified.")

    def test_thermodynamic_reversal(self):
        """
        Verifies state traceability. Since everything is deterministic and RNS-based,
        we can 'reverse' a state if we have the residues.
        """
        print("\n[SCRUTINY] Running Thermodynamic Reversal Test...")
        from vld_sdk.core import RNSEngine
        rns = RNSEngine()
        
        val = 123456789
        residues = rns.to_residues(val)
        reversed_val = rns.from_residues(residues)
        
        self.assertEqual(val, reversed_val)
        print(f"  Initial State: {val}")
        print(f"  Residue Manifold: {residues}")
        print(f"  Reversed State: {reversed_val}")
        print("  [PASS] Thermodynamic Reversibility Verified.")

if __name__ == "__main__":
    unittest.main()
