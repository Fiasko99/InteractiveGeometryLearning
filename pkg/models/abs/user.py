from abc import abstractmethod
from typing import Any, Dict

from pkg.models import users

__all__ = ["User"]


class User:
    __cookies: Dict[str, Any]

    @abstractmethod
    def __init__(self, u: users.User):
        self.__user = u
        raise NotImplementedError

    @abstractmethod
    def login(self):
        raise NotImplementedError

    @abstractmethod
    def logout(self):
        raise NotImplementedError

    @abstractmethod
    def get_tests(self):
        raise NotImplementedError

    @abstractmethod
    def check_tests(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def cookies(self):
        return self.__cookies
