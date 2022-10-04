from functools import partial

from pkg.handlers.content.themes import UiContentWindowImpl


class Connector(UiContentWindowImpl):
    """Служит для подключения ивентов нажатия на элемент к функциям-
    обработчикам."""

    def adjust_connection(self):
        self.practice_btn.clicked.connect(self._introduce_practice)

        self.home_page.clicked.connect(self.to_home)
        self.geometry_page.clicked.connect(partial(self._switch_themes, "geometry"))
        self.matrix_page.clicked.connect(partial(self._switch_themes, "matrix"))

        self.theme_section.clicked.connect(self._on_theme_section_clicked)
        self.theory_btn.clicked.connect(self._switch_on_theory)

        self.first_example_btn.clicked.connect(
            partial(self._introduce_example, self.first_example_btn)
        )
        self.second_exmple_btn.clicked.connect(
            partial(self._introduce_example, self.second_exmple_btn)
        )

        self.__gui_entry_point()

    def __gui_entry_point(self):
        """Отрисовать список тем."""
        self.fill_tree_view()
