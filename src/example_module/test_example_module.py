from .example_module import add_ex


def test_add():
    assert add_ex(2, 2) == 4
