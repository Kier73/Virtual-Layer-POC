import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.vm import ResonanceGuard

def test_rns_denoising():
    print("STRESS | Test 18: RNS Entropy Denoising (RG-Flow)")
    guard = ResonanceGuard(threshold=0.9)
    
    noisy_stream = [0.5, 0.55, 0.99, 0.45, 0.52] # 0.99 is a massive entropy spike
    print(f"  > Noisy Stream: {noisy_stream}")
    
    clean_stream = guard.neutralize_spike(noisy_stream)
    print(f"  > Clean Stream: {[f'{x:.2f}' for x in clean_stream]}")
    
    spike_damped = clean_stream[2] # The 0.99 value
    avg_others = (0.5+0.55+0.45+0.52)/4
    
    print(f"  > Spike 0.99 Damped To: {spike_damped:.4f}")
    
    # Check if the spike was pulled toward the mean
    assert spike_damped < 0.95, "Entropy spike not sufficiently damped"
    print("VERDICT: PASS (RG-Flow neutralized high-entropy outlier)")

if __name__ == "__main__":
    test_rns_denoising()
