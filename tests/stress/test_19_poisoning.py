import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer
import time

def test_poisoning():
    print("STRESS | Test 19: Manifold Poisoning Resilience")
    vl_honest = VirtualLayer(seed=0x123)
    
    algorithm = "Standard_Relay"
    inputs = 0xAAAA
    honest_res = 0x5555
    
    # 1. Establish an honest Law
    print("  > Establishing Honest Law...")
    vl_honest.run(algorithm, lambda x: honest_res, inputs)
    
    # 2. Attempt to 'Poison' with an adversarial update
    # In VLD, once a Law is induced, subsequent 'run' calls with the same name/input
    # skip execution and use the manifold. If an attacker tries to pass a DIFFERENT function:
    print("  > Attempting Adversarial Induction (Poison)...")
    poison_res = 0x6666
    reflected_res = vl_honest.run(algorithm, lambda x: poison_res, inputs)
    
    print(f"  > Reflected Result: {hex(reflected_res)} (Expected: {hex(honest_res)})")
    
    # Manifold should stick to the first induced Law (Immutability)
    assert reflected_res == honest_res, "Manifold law was overwritten by adversary"
    print("VERDICT: PASS (Manifold immutability prevents law poisoning)")

if __name__ == "__main__":
    test_poisoning()
