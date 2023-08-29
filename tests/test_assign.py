def test_assign_local():
    from contextmanaged_assign import assign

    x = 1

    assert x == 1
    with assign("x", 2):
        assert x == 2
    assert x == 1


def test_assign_attr():
    from contextmanaged_assign import assign

    class MyClass:
        attr = "original value"

    myobj = MyClass()

    assert myobj.attr == "original value"
    with assign("myobj.attr", "new value"):
        assert myobj.attr == "new value"
    assert myobj.attr == "original value"


def test_assign_string():
    from contextmanaged_assign import assign

    attr = "original value"

    assert attr == "original value"
    with assign("attr", "new value"):
        assert attr == "new value"
    assert attr == "original value"


def test_assign_dict():
    from contextmanaged_assign import assign

    d = {"a": 1}

    assert d["a"] == 1
    with assign("d['a']", 32):
        assert d["a"] == 32
    assert d["a"] == 1


def test_assign_list():
    from contextmanaged_assign import assign

    l = [1, 2, 3]

    assert l[0] == 1
    with assign("l[0]", 32):
        assert l[0] == 32
    assert l[0] == 1
