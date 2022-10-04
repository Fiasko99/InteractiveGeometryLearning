from abc import abstractmethod

__all__ = ["Task"]


class Task:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        ...

    @abstractmethod
    def calculate(self):
        raise NotImplementedError

    @abstractmethod
    def show(self):
        raise NotImplementedError
