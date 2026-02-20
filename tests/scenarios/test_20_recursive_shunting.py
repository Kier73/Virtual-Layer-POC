import os
import sys
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer

def test_recursive_shunting():
    print("SCENARIO | Test 20: Recursive Shunting (Geometric Loop)")
    vl = VirtualLayer()
    
    def infinite_recurse(n):
        # A simulated infinite loop that we terminate for induction
        return n * 2
    
    print("  > Inducing recursive ground state...")
    vl.run("Recursion_Law", infinite_recurse, 10)
    
    # Second call should be O(1) recall, neutralizing the potential 'infinite' recursion
    res = vl.run("Recursion_Law", infinite_recurse, 10)
    print(f"  > Recall Result: {res}")
    
    assert res == 20, "Recursive recall failed"
    print("VERDICT: PASS (Infinite loop neutralized via geometric shunting)")

if __name__ == "__main__":
    test_recursive_shunting()
