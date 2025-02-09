import abc
from typing import Optional, Tuple


class BaseCache(abc.ABC):
    @abc.abstractmethod
    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        raise NotImplementedError

    @abc.abstractmethod
    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:
        raise NotImplementedError
