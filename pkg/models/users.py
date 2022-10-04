from pydantic import SecretStr

from pkg import BaseClientModel

__all__ = ["User"]


class User(BaseClientModel):
    """Model for storage user data."""

    login: str
    password: SecretStr
