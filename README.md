# FastAPI-Cacher

An intuitive caching library for FastAPI inspired by Flask-Caching.
It uses decorators for easy endpoint caching, supports both **absolute** and **sliding window expiration** mechanisms.

## Installation

Install and update using pip

```bash
pip install -U fastapi-cacher
```

## Cache Types

Configured in the CacheConfig class:

```python
# Options: "SimpleCache", "RedisCache", "MongoCache", "MemCache"
cache_type = "SimpleCache"  # Default: "SimpleCache", 
```

#### `SimpleCache`

- Suitable for development and single-thread applications.
- Default cache type if cache_type is not specified or CacheConfig is not provided.

#### `RedisCache`

- Robust option for production environments.
- Supports distributed caching.
- Configuration requires specifying either `redis_url` or both `redis_host` and `redis_password`.

#### `MongoCache`

- Uses MongoDB's `expireAfterSeconds` index to automatically manage the expiration of cached entries.
- Requires a MongoDB connection URL.

#### `MemCache`

- Uses a Memcached server to store cached data.
- Specify `memcache_host` and `memcache_port`.

### Each cache type has specific attributes in the `CacheConfig` that need to be configured:

```python
from fastapi_cacher import CacheConfig

# For SimpleCache
cache_config = CacheConfig(
  cache_type="SimpleCache",
  simple_cache_threshold=100,  # Default: 100 (number of items to store in cache, before deleting the oldest)
)

# For RedisCache
cache_config = CacheConfig(
  cache_type="RedisCache",
  redis_url="redis://localhost:6379",  # either redis_url or redis_host, redis_port, redis_password
  redis_host="your_redis_host",
  redis_port=6379,  # Default: 6379
  redis_password="your_redis_password",
  redis_db=0,  # Default: 0
)

# For MongoCache
cache_config = CacheConfig(
  cache_type="MongoCache",
  mongo_url="mongodb://user:password@localhost:27017",
  mongo_database="fastapi_cache",
  mongo_collection="your_cache_collection",  # Default: "cache"
  mongo_direct_connection=False  # Default: False
)

# For MemCache
cache_config = CacheConfig(
  cache_type="MemCache",
  memcache_host="your_memcache_host",  # Default: ""
  memcache_port=11211,  # Default: 11211
  memcache_threshold=100  # Default: 100 (number of items to store in cache, before deleting the oldest)
)
```

## Generic CacheConfig Attributes with Defaults:

- `cache_type` (str) = `SimpleCache`: Sets the caching strategy (e.g., SimpleCache, RedisCache).
- `default_timeout` (int) = `300`: Default timeout in seconds if not specified in decorator.
- `app_space` (str) = `fastapi-cacher`: Namespace prefix for cache keys to avoid conflicts.
- `coder` (Coder) = `JsonCoder`: Serialization coder for caching.
- `sliding_expiration` (bool) = `False`: Sets the caching mechanism globally, if True, the expiration time will be reset
  on every access **(overwritten by the decorator if specified there)**.
- Time Constants (`ONE_HOUR`, `ONE_DAY`, etc.): Predefined time intervals in seconds for easy setup of expiration times.

### Example:

```python
cache_config = CacheConfig(
  cache_type="SimpleCache",
  default_timeout=600,
  app_space="my_app",
  sliding_expiration=True
)
```

## Usage

To use the caching functionality, decorate your FastAPI endpoints with the @cache.cached decorator.
Here are some examples for each type of cache:

```python
from asyncio import sleep

from fastapi import FastAPI, Request, Response
from fastapi_cacher import Cache, CacheConfig

app = FastAPI()
# Configuring with RedisCache; for settings of other cache types, see the CacheConfig section above.
cache_config = CacheConfig(
    cache_type="RedisCache",
    redis_host="your_redis_host",
    redis_password="your_redis_password",
    default_timeout=600,  # default if not specified in the decorator
    app_space="fastapi-cacher",
    sliding_expiration=False
)
cache = Cache(config=cache_config)


@app.get("/item/{item_id}")
@cache.cached(timeout=300,
              sliding_expiration=False,
              namespace="item_detail",
              query_params=True,
              json_body=False,
              require_auth_header=False)
async def get_item(request: Request, response: Response, item_id: int):
    """
    request parameter is required in the function signature for the cache to work.
    request and response parameters can be named differently:
    async def get_item(req: Request, resp: Response, item_id: int):
    """
    await sleep(3)
    return {"id": item_id, "name": "Item Name"}


@app.get("/items/")
@cache.cached(timeout=cache_config.ONE_HOUR,
              namespace="item_detail")
async def get_items(request: Request, response: Response):
    """
    request parameter is required in the function signature for the cache to work.
    request and response parameters can be named differently:
    async def get_item(req: Request, resp: Response, item_id: int):
    """
    await sleep(3)
    return {"id": 1, "name": "Item Name"}
```

### `cache.cached` decorator arguments with defaults:

- `timeout` (int) = `None`: Timeout in seconds. Set to `0` to never expire. If not specified, the default timeout
  from the cache config is used. A pre-calculated values in the cache_config can be used, e.g.,
  `cache_config.ONE_HOUR`, `cache_config.ONE_DAY`, etc.
- `sliding_expiration` (bool) = `None`: If True, the expiration time will be reset on every access. If set, it
  overwrites the cache_config setting.
- `namespace` (str) = `""`: Allows scoping of cache keys.
- `query_params` (book) = `True`: Consider URL query parameters for caching.
- `json_body` = `False`: Include requests JSON body in the cache string key.
- `require_auth_header` = `False`: Include the Authorization header in the cache string key.
  If set to True, the Authorization header is required in the request and if not present - Raises `HTTPException(401)`.

## More about the sliding expiration mechanism:

The sliding expiration mechanism resets the expiration time of a cached item each time it is accessed. This means the
item will only be deleted if it is not accessed for the specified timeout period.

- Global Setting: Set in `CacheConfig` to apply by default to all endpoints.
- Individual Setting: Can be overridden in the `cache.cached` decorator for specific endpoints.

### Clearing the Cache

#### Endpoints can be configured to clear the cache selectively or entirely.

```python
@app.post('/clear-cache/')
async def clear_cache(namespace: str = None, key: str = None):
    """
    Clears the cache.
  
    - `namespace`: Optional. The namespace of the cache to clear.
    - `key`: Optional. The specific key within the namespace to clear.
  
    If no parameters are provided, the entire cache will be cleared.
    example:
    http://domain/clear-cache/?namespace=test&key=specific-key
    """
    await cache.clear(namespace=namespace, key=key)
    return "Cache cleared!"
```

### Other `cache` methods:

```python
# set 
await cache.set(key="key", value="value", timeout=300)

# get
value = await cache.get(key="key")

# get with ttl
ttl, cached_result = await cache.get_with_ttl(key="key")
```

## Contributions

Contributions to the fastapi-cacher project are welcome. Please ensure to follow best practices for code quality and add
tests for new features.

## License

This project is licensed under the MIT License.

## Changelog

For all the changes and version history, see the [CHANGELOG](CHANGELOG.md).