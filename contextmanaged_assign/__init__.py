import re
import inspect
from contextlib import contextmanager


@contextmanager
def assign(varpath, tempval, /):
    """
    Temporarily assigning a value to a variable or attribute.
    The original value is restored when the context is exited.

    Example:
        with assign("myobj.x", 2):
            assert myobj.x == 2

    Note: `assign` can NOT modify local variables themselves. So this will NOT work:

    INVALID:
        x = 1
        with assign("x", 2):
            assert x == 2  # AssertionError: 1 != 2
        assert x == 1
    """

    @contextmanager
    def get_calling_frame():
        current_frame = inspect.currentframe()
        while current_frame:
            if (
                current_frame.f_globals.get("__name__") != __name__
                and current_frame.f_globals.get("__name__") != "contextmanaged_assign"
                and current_frame.f_globals.get("__name__") != "contextlib"
            ):
                break
            current_frame = current_frame.f_back

        yield current_frame

        # Force synchronization of f_locals with fast-locals
        current_frame.f_trace = lambda *args, **kwargs: None
        del current_frame

    is_atomic_local = re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", varpath)

    # get the original value
    with get_calling_frame() as calling_frame:
        original_value = eval(varpath, calling_frame.f_globals, calling_frame.f_locals)

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


__all__ = ["assign"]
