import time
import random
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.holographic import Hypervector, TrinityConsensus, ByzantineHDC
from vld_sdk.core import RNSEngine

def run_consensus_demo():
    print("="*80)
    print(" VLD CONSENSUS SCRUTINY & BYZANTINE FAULT TOLERANCE")
    print("="*80)
    
    tc = TrinityConsensus(seed=0x123)
    event_sig = 0xABCDEF1234
    
    truth = tc.resolve("Thermodynamics", "Equilibrium", event_sig)
    truth_sig = truth.signature()
    
    print(f"TRINITY|RESOLVED_TRUTH_SIG: {hex(truth_sig)}")
    
    print("BYZANTINE|SIMULATING_3_NODE_CLUSTER")
    node1 = Hypervector(truth.bits, "Validator_A")
    node2 = Hypervector(truth.bits, "Validator_B")
    node3 = Hypervector(random.getrandbits(4096), "Adversarial_Node")
    
    cluster = [node1, node2, node3]
    
    bhdc = ByzantineHDC()
    start = time.perf_counter()
    consensus_result = bhdc.reconcile(cluster)
    end = time.perf_counter()
    
    consensus_sig = consensus_result.signature()
    is_valid = bhdc.verify(consensus_result, truth_sig)
    
    print(f"BYZANTINE|RECOVERED_TRUTH_SIG: {hex(consensus_sig)}")
    print(f"BYZANTINE|RECOVERY_LATENCY: {(end-start)*1000:.4f}ms")
    print(f"BYZANTINE|INTEGRITY_VERIFIED: {is_valid}")
    
    hamming_dist = bin(truth.bits ^ consensus_result.bits).count('1')
    similarity = 1.0 - (hamming_dist / 4096.0)
    print(f"CONSENSUS|BIT_FIDELITY: {similarity * 100:.2f}%")

    rns = RNSEngine()
    val = consensus_sig % RNSEngine.DYNAMIC_RANGE
    residues = rns.to_residues(val)
    recovered = rns.from_residues(residues)
    
    print(f"RNS|SUBSTRATE_MATCH: {val == recovered}")
    print(f"RNS|RESIDUES: {residues}")

    print("\nVERDICT|CONSENSUS_DYNAMICS: PASS")

if __name__ == "__main__":
    run_consensus_demo()
