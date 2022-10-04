class NoMainArguments(Exception):
    """Класс который служит для создания ошибки.

    Вызывается в сулчае если контроллеру не переданны ключевые
    аргументы.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return (
            f"No main arguments: "
            f"[args={','.join(self.args)} | kwargs={','.join(self.kwargs)}"
        )
