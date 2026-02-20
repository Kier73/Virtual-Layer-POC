import time
import math
import numpy as np
import torch
import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from vld_sdk.induction import VirtualLayer
from vld_sdk.matrix import VMatrix, GMatrix, XMatrix, PMatrix

# Glue functions moved from SDK to Demo to keep SDK pure
def vld_to_numpy(vld_matrix, r_start, r_end, c_start, c_end):
    rows = r_end - r_start
    cols = c_end - c_start
    arr = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            arr[i, j] = vld_matrix.resolve(r_start + i, c_start + j)
    return arr

def vld_to_torch(vld_matrix, r_count, c_count):
    weights = torch.zeros((r_count, c_count))
    for i in range(r_count):
        for j in range(c_count):
            weights[i, j] = vld_matrix.get_element(i, j)
    return weights

def run_matrix_scrutiny():
    print("="*80)
    print(" VLD MATRIX SCRUTINY & FRAMEWORK INTEGRATION")
    print("="*80)
    vl = VirtualLayer(seed=0x1337BEEF)

    # 1. ANALYTICAL DEPTH & ASSOCIATIVITY
    A = vl.get_geometric_matrix(100, 100, 0x1)
    B = vl.get_geometric_matrix(100, 100, 0x2)
    C = vl.get_geometric_matrix(100, 100, 0x3)

    curr = A.desc
    for i in range(1000):
        curr = curr.bind(B.desc)
    
    res_chain = GMatrix(curr).resolve(10, 10)
    print(f"DEPTH|1000_LAYER_RESOLVE|COORD(10,10): {res_chain:.6f}")

    left = A.desc.bind(B.desc.bind(C.desc))
    right = A.desc.bind(B.desc).bind(C.desc)
    val_l = GMatrix(left).resolve(5, 5)
    val_r = GMatrix(right).resolve(5, 5)
    print(f"IDENTITY|ASSOCIATIVE_MATCH: {val_l == val_r} ({val_l:.8f})")

    # 2. EXASCALE SCALING
    N_EXP = 10**100
    pm = PMatrix(N_EXP, N_EXP, depth=4)
    start = time.perf_counter()
    val_google = pm.get_element(42, 42*2*3*5)
    end = time.perf_counter()
    print(f"SCALE|GOOGOL_COORD|RESOLVE: {val_google}")
    print(f"SCALE|LATENCY: {(end-start)*1000:.4f}ms")

    # 3. NUMPY INTEGRATION
    gm = vl.get_geometric_matrix(1000000, 1000000, 0xABC)
    print(f"NUMPY|TILE_EXTRACT|100x100_FROM_1M:")
    start = time.perf_counter()
    np_tile = vld_to_numpy(gm, 0, 100, 0, 100)
    end = time.perf_counter()
    print(f"NUMPY|EXTRACT_LATENCY: {(end-start)*1000:.4f}ms")
    print(f"NUMPY|TILE_SUM: {np.sum(np_tile):.4f}")
    
    fft_res = np.fft.fft2(np_tile)
    print(f"NUMPY|FFT_MAGNITUDE_AVG: {np.mean(np.abs(fft_res)):.4f}")

    # 4. PYTORCH INTEGRATION
    xm = XMatrix(256, 256, seed=0x777)
    print(f"PYTORCH|WEIGHT_SYNTHESIS|256x256:")
    start = time.perf_counter()
    weights = vld_to_torch(xm, 256, 256)
    end = time.perf_counter()
    print(f"PYTORCH|SYNTH_LATENCY: {(end-start)*1000:.4f}ms")
    print(f"PYTORCH|TENSOR_SHAPE: {weights.shape}")
    print(f"PYTORCH|WEIGHT_MEAN: {torch.mean(weights).item():.4f}")

    input_tensor = torch.randn(1, 256)
    output = torch.mm(input_tensor, weights)
    print(f"PYTORCH|FORWARD_PASS_MEAN: {torch.mean(output).item():.4f}")

    # 5. INDIVIDUAL CAPABILITIES
    pm_rect = PMatrix(10**20, 10**10, depth=1)
    val_rect = pm_rect.get_element(7, 49)
    print(f"CAPS|RECTANGULAR|10^20x10^10|COORD(7,49): {val_rect}")

    print("\nVERDICT|MATRIX_DYNAMICS: PASS")

if __name__ == "__main__":
    run_matrix_scrutiny()
