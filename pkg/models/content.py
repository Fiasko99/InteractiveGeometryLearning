from dataclasses import dataclass, field
from typing import Any, Dict, List

from pkg.handlers.content_parser import parse_content_data

__all__ = ["Content"]


@dataclass
class Content:
    """Класс, который служит для взаимодействия с `content.json`."""

    __theme_name: str = None
    __active_example: str = "first_example"
    __content_type: str = "geometry"
    content: Dict[str, Dict[str, Any]] = field(
        default_factory=lambda: parse_content_data()
    )

    def __str__(self):
        return (
            f"Content["
            f"theme_name={self.__theme_name} "
            f"content_type={self.__content_type} "
            f"content={self.content}]"
        )

    def __post_init__(self):
        self.__first_theme_name__()

    def __first_theme_name__(self):
        """Найти наименование первой темы и установить для `__theme_name`."""
        for theme_name in self.__parse_themes():
            if theme_name != "module":
                self.__theme_name = theme_name
                break

    def __parse_themes(self) -> List[str]:
        """Преобразовать объект контента в массив."""
        return list(self.content.get(self.__content_type, {}).keys())

    @property
    def code(self):
        return self.example["code"]

    @property
    def count_matrix(self) -> int:
        """Получить число доступных матриц."""
        return self.example["count_matrix"]

    @property
    def example_controller(self):
        """Получить контроллер для определенного примера."""
        return self.specific_content.get(self.__theme_name)["controller"]

    @property
    def module(self):
        """Получить модуль для определенной темы."""
        return self.specific_content["module"]

    @property
    def args(self):
        """Получить аргументы лдя контроллера."""
        return self.example["args"]

    @property
    def example_theory(self):
        """Получить теорию для определенного примера."""
        return self.example["theory"]

    @property
    def dimensional(self):
        return self.example["3d"]

    @property
    def example(self) -> Dict[str, Any]:
        """Получить данные по активному примеру."""
        return self.specific_content.get(self.__theme_name).get(self.__active_example)

    @property
    def theory(self):
        """Получить общую теорию для определенной темы."""
        return self.specific_content.get(self.__theme_name)["theory"]

    @property
    def themes(self) -> List[str]:
        """Получить название всех тем."""
        return [theme for theme in self.__parse_themes() if theme != "module"]

    @property
    def specific_content(self) -> Dict[str, Dict[str, Any]]:
        """Получить данные определенной темы из контента."""
        return self.content.get(self.__content_type, {})

    @property
    def practice(self):
        """Получить теорию практики."""
        return self.specific_content.get(self.__theme_name)["practice"]["theory"]

    @property
    def active_example(self):
        return self.__active_example

    @active_example.setter
    def active_example(self, button_text: str):
        self.__active_example = (
            "first_example" if button_text == "Пример 1" else "second_example"
        )

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, _type: str) -> None:
        self.__content_type = _type

    @property
    def theme_name(self):
        return self.__theme_name

    @theme_name.setter
    def theme_name(self, name) -> None:
        self.__theme_name = name
