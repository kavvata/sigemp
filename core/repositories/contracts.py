from abc import ABC, abstractmethod


class UserRepository(ABC):
    @abstractmethod
    def authenticate(username: str, password: str) -> any:
        pass
