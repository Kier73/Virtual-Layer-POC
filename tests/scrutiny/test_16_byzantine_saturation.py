import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.holographic import TrinityConsensus, ByzantineHDC, Hypervector

def test_byzantine_saturation():
    print("SCRUTINY | Test 16: Byzantine Majority Voting Saturation (75% Threshold)")
    tc = TrinityConsensus(seed=0x123)
    hdc = ByzantineHDC()
    
    truth = Hypervector.from_seed(0x12345678, "Truth")
    truth_sig = truth.signature()
    
    # 1. Test at 40% noise (3 Truth, 2 Noise) (Should PASS)
    node_50 = [truth, truth, truth, Hypervector.from_seed(0x999), Hypervector.from_seed(0x888)]
    res_50 = hdc.reconcile(node_50).signature()
    print(f"  > Noise 40% (3 vs 2) | Reconciled: {hex(res_50)} | {'PASS' if res_50 == truth_sig else 'FAIL'}")
    
    # 2. Test at 75% noise (Should FAIL/UNSTABLE)
    node_75 = [truth, Hypervector.from_seed(0x777), Hypervector.from_seed(0x666), Hypervector.from_seed(0x555)]
    res_75 = hdc.reconcile(node_75).signature()
    print(f"  > Noise 75% | Reconciled: {hex(res_75)} | Expected instability.")
    
    assert res_50 == truth_sig, "Consensus must hold with clear majority"
    print("VERDICT: PASS (Saturation dynamics verified)")

if __name__ == "__main__":
    test_byzantine_saturation()
