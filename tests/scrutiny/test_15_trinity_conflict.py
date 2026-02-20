import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.holographic import TrinityConsensus, ByzantineHDC

def test_trinity_conflict():
    print("SCRUTINY | Test 15: Trinity Reconciliation (Logic vs Intention vs Event)")
    tc = TrinityConsensus(seed=0x999)
    hdc = ByzantineHDC()
    
    # Correct state
    event_sig = 0xAA11
    truth = tc.resolve("Logic", "State", event_sig)
    
    print(f"  > Baseline Truth Signature: {hex(truth.signature())}")
    
    # Reconcile with 1 corrupted source (33% noise)
    # Simulation: 2 honest nodes, 1 liar
    from vld_sdk.holographic import Hypervector
    liar = Hypervector.from_seed(0xBAD1, "Liar")
    node_results = [truth, truth, liar] 
    
    reconciled = hdc.reconcile(node_results)
    reconciled_sig = reconciled.signature()
    print(f"  > Reconciled Signature:     {hex(reconciled_sig)}")
    
    assert reconciled_sig == truth.signature(), "ByzantineHDC must resolve truth with 33% conflict"
    print("VERDICT: PASS (Trinity Reconciliation holds at 1/3 corruption)")

if __name__ == "__main__":
    test_trinity_conflict()
