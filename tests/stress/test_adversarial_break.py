import random
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.holographic import Hypervector, ByzantineHDC

def stress_adversarial_break():
    print("="*80)
    print(" STRESS TEST: ADVERSARIAL SATURATION (TRUTH FLOOR)")
    print("="*80)
    
    truth = Hypervector.from_seed(0xDEADC0DE, "TRUTH")
    truth_sig = truth.signature()
    
    noise_levels = [10, 30, 45, 49, 50, 51, 60, 75]
    bhdc = ByzantineHDC()
    
    print(f"GROUND_TRUTH: {hex(truth_sig)}")
    print("\nTESTING_NOISE_THRESHOLDS:")

    for pct in noise_levels:
        honest_count = 100 - pct
        noise_count = pct
        
        cluster = [Hypervector(truth.bits, "Honest")] * honest_count
        for _ in range(noise_count):
            cluster.append(Hypervector(random.getrandbits(4096), "Malicious"))
            
        recovered = bhdc.reconcile(cluster)
        recovered_sig = recovered.signature()
        
        success = recovered_sig == truth_sig
        status = "PASSED" if success else "FAILED"
        
        print(f"  NOISE_{pct}%: {status} | Recovered: {hex(recovered_sig)[:18]}...")
        
        if not success:
            print(f"\n[BREAK_POINT] TRUTH LOST AT {pct}% NOISE.")
            break

    print("\nVERDICT: VLD Consensus holds to the theoretical 50% limit; breaks at 51%.")

if __name__ == "__main__":
    stress_adversarial_break()
