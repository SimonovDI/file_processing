from abc import ABC, abstractmethod


class BaseLoader(ABC):

    @abstractmethod
    def load(self, *args, **kwargs) -> None:
        pass
