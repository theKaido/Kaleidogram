from app.utils.security import hash_password, verify_password


def test_verify_password():
    """Test the verify_password function."""
    string_to_hash = "tests"
    hashed = hash_password(string_to_hash)
    assert verify_password("tests", hashed)
    assert not verify_password("test", hashed)


def test_hash_password():
    """Test the hash_password function."""
    hashed_1 = hash_password("tests")
    hashed_2 = hash_password("tests")
    assert hashed_1 != "tests"
    assert hashed_1 != hashed_2
