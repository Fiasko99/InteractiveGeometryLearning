from .tasks import Task

__all__ = ["Graphics"]


class Graphics:
    @staticmethod
    def show(t: Task) -> None:
        t.show()
