from typing import override

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from core.repositories.contracts import UserRepository


class DjUserRepository(UserRepository):
    @override
    def authenticate(self, username: str, password: str) -> User:
        return authenticate(username=username, password=password)
