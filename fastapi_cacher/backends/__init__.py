__all__ = ["Backend", "inmemory"]

# import each backend in turn and add to __all__. This syntax
# is explicitly supported by type checkers, while more dynamic
# syntax would not be recognised.
try:
    from fastapi_cacher.backends import dynamodb
except ImportError:
    pass
else:
    __all__ += ["dynamodb"]

try:
    from fastapi_cacher.backends import memcached
except ImportError:
    pass
else:
    __all__ += ["memcached"]

try:
    from fastapi_cacher.backends import redis
except ImportError:
    pass
else:
    __all__ += ["redis"]
