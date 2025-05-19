from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> any:
        pass
