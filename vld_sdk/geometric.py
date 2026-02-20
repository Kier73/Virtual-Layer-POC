"""
VLD-GEOMETRIC: Manifold Mapping
Brief: Tools for spatial grounding (Hilbert) and modular-to-continuous projection (Torus).

Notation:
    [Hilbert] (x, y) <-> d (Manifold Index)
    [Torus] T(x) = { sum(ri/mi) } mod 1
"""
import math
from typing import Tuple

class HilbertGrounding:
    """
    Maps 2D spatial coordinates (x, y) to a 1D manifold index using the Hilbert Curve.
    Ensures spatial locality for multi-dimensional data patterns.
    """
    @staticmethod
    def xy_to_d(n: int, x: int, y: int) -> int:
        d = 0
        s = n // 2
        while s > 0:
            rx = (x & s) > 0
            ry = (y & s) > 0
            d += s * s * ((3 * rx) ^ ry)
            x, y = HilbertGrounding._rotate_flip(s, x, y, rx, ry)
            s //= 2
        return d

    @staticmethod
    def d_to_xy(n: int, d: int) -> Tuple[int, int]:
        t = d
        x = y = 0
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            x, y = HilbertGrounding._rotate_flip(s, x, y, rx, ry)
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        return x, y

    @staticmethod
    def _rotate_flip(n: int, x: int, y: int, rx: int, ry: int) -> Tuple[int, int]:
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            return y, x
        return x, y

class TorusProjector:
    """
    Converts RNS residues into a fractional summation (Analytic Induction).
    Maps points from the modular residue space to a continuous Torus manifold [0, 1].
    """
    @staticmethod
    def project(residues: list[int], moduli: list[int]) -> float:
        accumulator = 0.0
        for r, m in zip(residues, moduli):
            accumulator += float(r) / float(m)
        # Return fractional part (The Torus mapping)
        return accumulator - math.floor(accumulator)

if __name__ == "__main__":
    # Test Hilbert
    n = 64 # Grid size must be power of 2
    d = HilbertGrounding.xy_to_d(n, 10, 10)
    print(f"Hilbert (10,10) on {n}x{n} grid -> Index {d}")
    
    # Test Torus
    res = [10, 20, 30]
    mods = [251, 257, 263]
    val = TorusProjector.project(res, mods)
    print(f"Torus Projection of {res} mod {mods} -> {val:.6f}")
