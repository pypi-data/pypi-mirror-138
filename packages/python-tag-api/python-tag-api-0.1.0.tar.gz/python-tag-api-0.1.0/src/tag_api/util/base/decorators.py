import functools
from .excpetions import UnauthorizedException

def retry_if_unauthorized(func):
        functools.wraps(func)
        def wrapper(ref, *args, **kwargs):
            try:
                return func(ref, *args, **kwargs)
            except UnauthorizedException:
                ref._authorize()
                return func(ref, *args, **kwargs)
        return wrapper
