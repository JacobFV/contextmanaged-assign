# ContextManaged Assign

This Python project provides a context manager for temporarily assigning a value to a variable or attribute. The original value is restored when the context is exited.

## Usage

```python
from contextmanaged_assign import assign

l = [1, 2, 3]

assert l[0] == 1
with assign("l[0]", 2):
    assert l[0] == 2
assert l[0] == 1
```

Please note that `assign` cannot modify local variables themselves. For example, the following code will not work:

```python
x = 1
with assign("x", 2):
    assert x == 2  # AssertionError: 1 != 2
assert x == 1
```

## Installation

Simply install the package using `pip`:

```bash
pip install contextmanaged-assign
```

Then import the `assign` function from the `contextmanaged-assign` module.

## License

[MIT](LICENSE)