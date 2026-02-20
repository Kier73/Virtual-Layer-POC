import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.matrix import PMatrix

def test_p_divisor_chain():
    print("SCRUTINY | Test 04: P-Series Divisor Chain Depth")
    pm = PMatrix(100, 100)
    
    # Check chain stability
    factors = pm._get_factors(123456789)
    print(f"  > Factors (123456789): {factors}")
    
    # Product of factors should equal the number
    prod = 1
    for p, exp in factors.items(): prod *= (p ** exp)
    
    print(f"  > Product Matching: {prod == 123456789}")
    assert prod == 123456789, "Divisor chain product must be exact"
    print("VERDICT: PASS (Deep Integer Resolution Maintained)")

if __name__ == "__main__":
    test_p_divisor_chain()
