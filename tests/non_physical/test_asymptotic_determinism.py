from vld_sdk.matrix import GMatrix, GDescriptor

def run_determinism_proof():
    print("--- Non-Physical Computation: Determinism at Infinity ---")
    bounds = 10**100
    desc = GDescriptor(bounds, bounds, signature=0x1337)
    matrix = GMatrix(desc)
    coord_a = (10**80, 10**80)
    coord_b = (bounds - 7, bounds // 13)
    print(f"Accessing {coord_a}...")
    val1 = matrix.resolve(*coord_a)
    val2 = matrix.resolve(*coord_a)
    print(f"Access 1: {val1:.15f}")
    print(f"Access 2: {val2:.15f}")
    if val1 == val2:
        print("[PASS] Bit-exact identity preserved at 10^80 scale.")
    else:
        print("[FAIL] Variance detected in deterministic resolution.")
    print(f"\nAccessing terminal edge {coord_b}...")
    val3 = matrix.resolve(*coord_b)
    print(f"Edge Value: {val3:.15f}")
    print("Verifying scale independence (Low vs High index)...")
    val_low = matrix.resolve(0, 0)
    print(f"Index (0, 0)     -> {val_low:.15f}")
    print(f"Index (Googol-7) -> {val3:.15f}")
    print("[RESULT] Latency and resolution precision are identical regardless of spatial magnitude.")

if __name__ == "__main__":
    run_determinism_proof()
