from vld_sdk.core import DeterministicHasher, FeistelMemoizer, RNSEngine, NTTEngine

def test_hasher():
    h = DeterministicHasher()
    assert h.hash_data("test") == h.hash_data("test")
    assert h.hash_data([1.0, 2.0]) != h.hash_data([1.0, 2.1])

def test_feistel():
    f = FeistelMemoizer()
    c = 0x1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF
    s1 = f.project_to_seed(c)
    s2 = f.project_to_seed(c)
    assert s1 == s2
    assert isinstance(s1, int)

def test_rns():
    val = 12345678901234567890
    residues = RNSEngine.to_residues(val)
    recovered = RNSEngine.from_residues(residues)
    assert val == recovered

def test_ntt_behavior():
    # Verify deterministic mapping of NTT simulation
    data = [1, 2, 3, 4]
    mod = 251
    t1 = NTTEngine.transform(data, mod)
    t2 = NTTEngine.transform(data, mod)
    assert t1 == t2
    assert len(t1) == len(data)

if __name__ == "__main__":
    print("Running Tests...")
    try:
        test_hasher()
        print("Hasher: OK")
        test_feistel()
        print("Feistel: OK")
        test_rns()
        print("RNS: OK")
        test_ntt_behavior()
        print("NTT: OK")
        print("\nAll Tests Passed!")
    except Exception as e:
        print(f"Test Failed: {e}")
