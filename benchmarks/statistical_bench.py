import numpy as np
from scipy import stats
import math
from vld_sdk.matrix import GMatrix, GDescriptor, VMatrix

def test_uniformity():
    print("--- Statistical Uniformity: GMatrix ---")
    desc = GDescriptor(100, 100, signature=0xABC)
    matrix = GMatrix(desc)
    samples = []
    for i in range(100):
        for j in range(100):
            samples.append(matrix.resolve(i, j))
    samples = np.array(samples)
    samples_unit = (samples + 1.0) / 2.0
    d_stat, p_val = stats.ks_1samp(samples_unit, stats.uniform.cdf)
    print(f"KS Test: D={d_stat:.4f}, p-value={p_val:.4f}")
    if p_val > 0.05:
        print("[PASS] Distribution is indistinguishable from Uniform (p > 0.05)")
    else:
        print("[FAIL] Distribution departs from Uniform (p <= 0.05)")

def test_jl_lemma():
    print("\n--- JL Lemma: Pairwise Distance Preservation ---")
    in_dim = 1000
    out_dim = 100
    n_vectors = 50
    vm = VMatrix(seed=42)
    vectors = [np.random.randn(in_dim).tolist() for _ in range(n_vectors)]
    orig_dists = []
    for i in range(n_vectors):
        for j in range(i + 1, n_vectors):
            dist = np.linalg.norm(np.array(vectors[i]) - np.array(vectors[j]))
            orig_dists.append(dist)
    projected = [vm.project(v, out_dim) for v in vectors]
    proj_dists = []
    for i in range(n_vectors):
        for j in range(i + 1, n_vectors):
            dist = np.linalg.norm(np.array(projected[i]) - np.array(projected[j]))
            proj_dists.append(dist)
    ratios = np.array(proj_dists) / np.array(orig_dists)
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    print(f"Mean distance ratio (Projected/Original): {mean_ratio:.4f}")
    print(f"Std dev of ratio: {std_ratio:.4f}")
    epsilon = 0.2
    success_rate = np.sum((ratios > (1-epsilon)) & (ratios < (1+epsilon))) / len(ratios)
    print(f"Distances preserved within {epsilon*100}% epsilon: {success_rate*100:.2f}%")
    if success_rate > 0.8:
        print("[PASS] Pairwise distances preserved within JL bounds.")
    else:
        print("[FAIL] Distance preservation failed JL criteria.")

if __name__ == "__main__":
    test_uniformity()
    test_jl_lemma()
