import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.core import FeistelMemoizer

def test_feistel_diffusion():
    print("STRESS | Test 09: Feistel Hashing Diffusion (Avalanche Effect)")
    fm = FeistelMemoizer(rounds=4)
    
    base_coord = 0xAA55AA55AA55AA55
    res_base = fm.project_to_seed(base_coord)
    
    total_bits = 64
    total_flipped = 0
    
    print(f"  > Probing 1-bit flips in 64-bit coordinate...")
    for i in range(total_bits):
        flipped_coord = base_coord ^ (1 << i)
        res_flipped = fm.project_to_seed(flipped_coord)
        # Count flipped bits in output
        diff = res_base ^ res_flipped
        flipped_bits = bin(diff).count('1')
        total_flipped += flipped_bits
        
    avg_flipped = total_flipped / total_bits
    avalanche = (avg_flipped / 64) * 100
    print(f"  > Average Bits Flipped: {avg_flipped:.2f}")
    print(f"  > Avalanche Effect:    {avalanche:.2f}%")
    
    # Avalanche should be near 50%
    assert 40 < avalanche < 60, f"Avalanche effect too weak: {avalanche}%"
    print("VERDICT: PASS (Feistel Cipher provides high entropy diffusion)")

if __name__ == "__main__":
    test_feistel_diffusion()
