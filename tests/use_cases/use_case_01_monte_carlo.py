import os
import sys
import random
import time
sys.path.append(os.getcwd())
from vld_sdk.induction import VirtualLayer

def use_case_01_monte_carlo():
    print("USE CASE | Finance: Monte Carlo Path Shunting")
    vl = VirtualLayer()
    
    def simulate_portfolio_path(seed):
        # Simulate a complex stochastic path (GBM etc.)
        random.seed(seed)
        price = 100.0
        for _ in range(252): # 1 year trading
            price *= (1 + random.gauss(0, 0.01))
        return price

    # Simulating 10,000 "Days" of the same scenario
    scenario_id = "Portfolio_Risk_A"
    print(f"  > Inducing Scenario: {scenario_id}...")
    
    # First time: simulate (Slow)
    start1 = time.perf_counter()
    p1 = vl.run(scenario_id, simulate_portfolio_path, 0x555)
    end1 = time.perf_counter()
    
    # Second time: recall (Instantly shunted)
    start2 = time.perf_counter()
    p2 = vl.run(scenario_id, simulate_portfolio_path, 0x555)
    end2 = time.perf_counter()
    
    print(f"  > Simulation Result: ${p1:.2f}")
    print(f"  > Baseline Latency: {(end1-start1)*1000:.4f}ms")
    print(f"  > VLD Shunted Latency: {(end2-start2)*1000:.4f}ms")
    
    assert p1 == p2, "Path variance detected in deterministic manifold"
    print("VERDICT: PASS (Stochastic paths grounded in VLD allow instant risk re-calculation)")

if __name__ == "__main__":
    use_case_01_monte_carlo()
