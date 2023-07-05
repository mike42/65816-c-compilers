from backend.util import compiler_exists


def test_compiler_exists():
    assert compiler_exists('bash')
    assert not compiler_exists('cc68k_not_real')
