import time
import numpy as np
from scipy import sparse
import math
from vld_sdk.matrix import GMatrix, GDescriptor

def benchmark_throughput():
    print("--- Throughput: VLD vs. Scipy.Sparse ---")
    size = 10**6 # 1M elements
    dim = int(math.sqrt(size))
    sparsity = 0.01 # 1% non-zero
    nnz = int(size * sparsity)
    rows = np.random.randint(0, dim, nnz)
    cols = np.random.randint(0, dim, nnz)
    data = np.random.rand(nnz)
    t1 = time.perf_counter()
    s_mat = sparse.csr_matrix((data, (rows, cols)), shape=(dim, dim))
    t2 = time.perf_counter()
    print(f"Scipy.Sparse Build Time: {t2 - t1:.4f}s")
    access_coords = [(np.random.randint(0, dim), np.random.randint(0, dim)) for _ in range(10000)]
    t1 = time.perf_counter()
    for r, c in access_coords:
        _ = s_mat[r, c]
    t2 = time.perf_counter()
    scipy_lat = (t2 - t1) / 10000
    desc = GDescriptor(dim, dim, signature=0x123)
    matrix = GMatrix(desc)
    t1 = time.perf_counter()
    for r, c in access_coords:
        _ = matrix.resolve(r, c)
    t2 = time.perf_counter()
    vld_lat = (t2 - t1) / 10000
    print(f"Scipy.Sparse Avg Access: {scipy_lat*1000000:.2f} us")
    print(f"VLD GMatrix  Avg Access: {vld_lat*1000000:.2f} us")
    print(f"\nThroughput (Resolutions/sec):")
    print(f"VLD: {1.0/vld_lat:,.0f} elements/sec")

if __name__ == "__main__":
    benchmark_throughput()
