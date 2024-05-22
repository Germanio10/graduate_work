from abc import ABC, abstractmethod


class AbstractCacheRepository(ABC):
    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: str):
        pass
