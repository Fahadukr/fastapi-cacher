from typing import Literal, get_args, Final

from fastapi_cacher.coder import JsonCoder, Coder
from pydantic import BaseModel, model_validator, field_validator

SUPPORTED_CACHE_TYPES = Literal["SimpleCache", "RedisCache", "MongoCache", "MemCache"]


class CacheConfig(BaseModel):
    cache_type: SUPPORTED_CACHE_TYPES = "SimpleCache"
    default_timeout: int = 300
    app_space: str = "fastapi-cacher"
    coder: Coder = JsonCoder
    sliding_expiration: bool = False  # if True, the expiration time will be reset on every access
    ONE_HOUR: Final[int] = 3600
    ONE_DAY: Final[int] = ONE_HOUR * 24
    ONE_WEEK: Final[int] = ONE_DAY * 7
    ONE_MONTH: Final[int] = ONE_DAY * 30
    ONE_YEAR: Final[int] = ONE_DAY * 365

    simple_cache_threshold: int = 100

    redis_url: str = ""
    redis_host: str = None
    redis_port: int = 6379
    redis_password: str = None
    redis_db: int = 0

    mongo_url: str = ""
    mongo_database: str = "fastapi-cacher"
    mongo_collection: str = "cache"
    mongo_direct_connection: bool = False

    memcache_host: str = ""
    memcache_port: int = 11211
    memcache_threshold: int = 100

    @field_validator('cache_type')
    def validate_cache_type(cls, value):
        """validate that the cache_type is supported"""
        if value not in get_args(SUPPORTED_CACHE_TYPES):
            raise ValueError(f'cache_type must be one of {SUPPORTED_CACHE_TYPES}')
        return value

    @model_validator(mode='after')
    def validate_connection_attributes(cls, values):
        if values.cache_type == 'RedisCache':
            if not values.redis_url and not all([values.redis_host, values.redis_password]):
                raise ValueError(
                    'With RedisCache, either redis_url must be provided or (redis_host, '
                    'redis_password) must be provided.'
                )

        elif values.cache_type == 'MongoCache':
            if not values.mongo_url:
                raise ValueError('With MongoCache, either mongo_url must be provided.')

        elif values.cache_type == 'MemCache':
            if not values.memcache_host:
                raise ValueError('With Memcache, memcache_host must be provided.')

        return values

    class Config:
        arbitrary_types_allowed = True
