import inspect
from functools import wraps
from unittest import mock


def mock_argv(*cli_args):
    def decorator(obj):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            # Empty string as first argument to match python CLI parsing
            with mock.patch('sys.argv', [''] + list(cli_args)):
                obj(*args, **kwargs)

        if inspect.isclass(obj):
            for name, method in inspect.getmembers(obj, inspect.isfunction):
                if name.startswith('test_'):
                    setattr(obj, name, decorator(method))
            return obj
        else:
            return wrapper
    return decorator
