__all__ = ["ABCBuilder"]

from ...controllers import *
from ...models.content import Content

_ = graphic_controllers  # noqa: F405, to ensure the use graphic_controllers and matrix_controllers.


class ABCBuilder:
    """Абстрактный сброщик.

    Служит для вызова контроллеров (поле `controller`) в `content.json`.
    """

    content: Content

    callback_function_prefix: str = ""

    def entry_point_builder(self, parent: str, content: Content, *args, **kwargs):
        """Точка входа для сборщика.

        :param parent: Ключевой параметр в `kwargs`, который ожидает контроллер.
        :param content: Класс-клиент для `content.json`
        :param args: Не именные аргументы.
        :param kwargs: Именные аргументы.
        """
        self.content = content

        self.__run_controller(
            parent,
            *args,
            **kwargs,
        )

    def __run_controller(self, parent, *args, **kwargs):
        """Объединяет используя разделитель `.` `controller` и `module` в
        `content.json`. -> module.controller.

        В результате исполнения (eval), мы получаем класс контроллера,
            которому передаем значения по ключу из `kwargs` (ex. axes), удаляем из
            kwargs ключ, что бы он не передавался дальше и обращаемся функции,
            в зависимости от выбранного примера
            (
                Если выбран
                    `Пример 1` - PREFIX_first_example
                        или
                    `Пример 2` - PREFIX_second_example
            ) вызывается функция, которой мы передаем *args и **kwargs.

        Пример результата объединения:
            graphics_controllers.ThemeOneController(axes).draw_first_example(*args, **kwargs)
                 ^                   ^               ^      ^        ^
                 |                   |               |      |        |
             `module`          `controller`      `parent` `prefix` `example`
        """
        return getattr(
            eval(f"{self.content.module}.{self.content.example_controller}")(
                kwargs.pop(parent, None)
            ),  # nosec: B307
            f"{self.callback_function_prefix}{self.content.active_example}",
        )(*args, **kwargs)
