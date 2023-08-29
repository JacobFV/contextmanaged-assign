import re
import inspect
from contextlib import contextmanager


@contextmanager
def assign(varpath, tempval, /):
    """
    This class provides a context manager for temporarily assigning a value to a variable or attribute.
    The original value is restored when the context is exited.
    """

    @contextmanager
    def get_calling_frame():
        # Adjust the frame level to get the correct calling frame
        get_calling_frame_frame = inspect.currentframe()
        get_calling_frame_contextmanager_frame = get_calling_frame_frame.f_back
        assign_frame = get_calling_frame_contextmanager_frame.f_back
        assign_contextmanager_frame = assign_frame.f_back
        assign_calling_frame = assign_contextmanager_frame.f_back

        yield assign_calling_frame

        # Force synchronization of f_locals with fast-locals
        assign_calling_frame.f_trace = lambda *args, **kwargs: None
        del assign_calling_frame

    is_atomic_local = re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", varpath)

    # get the original value
    with get_calling_frame() as calling_frame:
        original_value = eval(varpath, calling_frame.f_globals, calling_frame.f_locals)

    def trace(frame, event, arg):
        return None

    # set the new value
    with get_calling_frame() as calling_frame:
        if is_atomic_local:
            calling_frame.f_locals[varpath] = tempval
        else:
            exec(
                f"{varpath} = tempval",
                calling_frame.f_globals,
                {**calling_frame.f_locals, "tempval": tempval},
            )
        # Force synchronization of f_locals with fast-locals
        calling_frame.f_trace = trace

    try:
        yield

    finally:
        # restore the original value
        with get_calling_frame() as calling_frame:
            if is_atomic_local:
                calling_frame.f_locals[varpath] = original_value
            else:
                exec(
                    f"{varpath} = original_value",
                    calling_frame.f_globals,
                    {**calling_frame.f_locals, "original_value": original_value},
                )
            # Force synchronization of f_locals with fast-locals
            calling_frame.f_trace = trace


# Testing the function


# w
w = 1
print("w", w)
assert w == 1
with assign("w", 32):
    print("w", w)
    assert w == 32
print("w", w)
assert w == 1


def test_x():
    # x
    x = 1
    print("x", x)
    assert x == 1
    with assign("x", 32):
        print("x", x)
        assert x == 32
    print("x", x)
    assert x == 1


test_x()

y = [1, 2, 3]


def test_y():
    # y[0]
    print("y[0]", y[0])
    assert y[0] == 1
    with assign("y[0]", 32):
        print("y[0]", y[0])
        assert y[0] == 32
    print("y[0]", y[0])
    assert y[0] == 1


test_y()


def test_z():
    # z["a"]
    z = {"a": 1}
    print('z["a"]', z["a"])
    assert z["a"] == 1
    with assign("z['a']", 32):
        print('z["a"]', z["a"])
        assert z["a"] == 32
    print('z["a"]', z["a"])
    assert z["a"] == 1


test_z()
