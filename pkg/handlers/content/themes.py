from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from pkg.controllers import matrix_controllers
from pkg.gui.views import Ui_spa_app
from pkg.handlers.builders import GraphicsBuilder, MatrixBuilder
from pkg.handlers.content.home import UiHomeWindowImpl
from pkg.handlers.message import show_input_value_error
from pkg.handlers.paths import resource_path
from pkg.models import StandardItem
from pkg.models.canvas import MplCanvas
from pkg.models.content import Content

_ = matrix_controllers  # noqa: F405, to ensure the user matrix_controllers.


class UiContentWindowImpl(QMainWindow, Ui_spa_app):
    """Класс приложения основного окна с графиками и матрицами Класс содержит в
    себе родителей: PyQt приложение для инициализации окна и дизайн окна
    (Полное имя User Interface Single Page Application)"""

    # Класс полотна для графиков
    home_window: UiHomeWindowImpl
    canvas: MplCanvas

    # Класс загрузки контента по умолчанию
    content: Content = Content()

    # Классы построения математики для каждого из разделов,
    # которые распределяют активацию функций согласно теме и номеру примера
    graphic_builder: GraphicsBuilder = GraphicsBuilder()
    matrix_builder: MatrixBuilder = MatrixBuilder()

    # Массив заполнителей (матриц или параметров для графиков в зависимости от раздела) для чтения
    text_fields_array = []

    def __init__(self):
        """Инициализатор параметров класса который наследует родителей."""
        super().__init__()
        self.setupUi(self)
        # Иконка приложения
        self.setWindowIcon(QtGui.QIcon(self.__image_path_builder("icon.jpg")))

    @staticmethod
    def __image_path_builder(image_name):
        """Генератор для пути к файлам картинок."""
        return resource_path("assets", "images", image_name)

    def to_home(self):
        """Переход к странице с информацией о разработчике."""
        self.home_window = UiHomeWindowImpl()
        self.home_window.show()
        self.hide()

    def _switch_themes(self, content_type):
        """Переключатель разделов при нажатии."""
        self.content.content_type = content_type
        self.content.__first_theme_name__()
        # Повтороное заполнение списка тем с преварительным очищением для каждого из разделов
        self.fill_tree_view()

    def fill_tree_view(self):
        """Заполняет виджет списка тем для перехода к ним."""
        self.__clear_box(self.layout_SArea)
        tree_model = QStandardItemModel()
        root_node = tree_model.invisibleRootItem()
        for theme_name in self.content.themes:
            item: StandardItem = StandardItem(theme_name)
            root_node.appendRow(item)
        self.theme_section.setModel(tree_model)
        self.theme_section.expandAll()
        # Заполнитель теории по умолчанию первой темы в списке тем
        self.__introduce_content(self.content.theory)

    def _on_theme_section_clicked(self, item):
        """Функция для изменения данных контента при переключении на другую
        тему при нажатии на объект в списке тем."""
        self.__clear_box(self.layout_SArea)
        self.content.theme_name = item.data()
        self.__introduce_content(self.content.theory)

    def _switch_on_theory(self):
        """Переход к теории темы."""
        self.__clear_box(self.layout_SArea)
        self.__introduce_content(self.content.theory)

    def introduce_code(self):
        """Показывает аргумент code из файла json в скролл с примером."""
        group_box = QGroupBox("Код примера", self)
        layout_groupbox = QVBoxLayout(group_box)
        code = QTextEdit()
        code.setReadOnly(True)
        code.setStyleSheet("QTextEdit{background: none; border: none;}")
        text = self.content.code
        for string in text.split("\n"):
            code.append(string)
        font = code.document().defaultFont()
        fontMetrics = QtGui.QFontMetrics(font)
        textSize = fontMetrics.size(0, text)

        textWidth = textSize.width() + 30
        textHeight = textSize.height() + 30

        code.setMinimumSize(textWidth, textHeight)
        code.resize(textWidth, textHeight)
        layout_groupbox.addWidget(code)
        self.layout_SArea.addWidget(group_box)

    def __introduce_content(self, theory_data, header: str = "Теория:"):
        """Заполнитель контента для всех разделов внутри темы (Теория, Примеры
        и Практика)"""
        group_box = QGroupBox(header, self)
        layout_groupbox = QVBoxLayout(group_box)
        for theme in theory_data:
            if (_theme := theme.split(" "))[0] == "'p":
                image_path = self.__image_path_builder(_theme[1])
                label_image = QLabel()
                picture = QPixmap(image_path)
                label_image.setPixmap(picture)
                layout_groupbox.addWidget(label_image)
            else:
                text = QLabel(str(theme))
                layout_groupbox.addWidget(text)
        self.layout_SArea.addWidget(group_box)

    def _introduce_practice(self):
        """Функция перехода к разделу практики в теме."""
        self.__clear_box(self.layout_SArea)
        self.__introduce_content(self.content.practice, "Практика: ")

    def _introduce_example(self, btn):
        """Инициализация практики вне зависимости от номера практики
        Рассматривает основной раздел для исключительного построения
        полотна."""
        self.text_fields_array.clear()
        self.__clear_box(self.layout_SArea)
        self.content.active_example = btn.text()
        if self.content.content_type == "geometry":
            self._build_content_geometry()
        elif self.content.content_type == "matrix":
            self._build_content_matrix()
        self.introduce_code()

    def _build_content_matrix(self, h=3, w=4):
        """Генерирует контент темы с предварительной очисткой массива
        данных."""
        self.text_fields_array.clear()
        self.__clear_box(self.layout_SArea)
        self._build_matrix_grid(h, w)
        self.__introduce_content(self.content.example_theory)

    def _build_matrix_grid(self, h, w):
        """Строит сетку для матриц с определенной размерностью относительно
        указанного количества матриц в теме."""
        group_box = QGroupBox("Матрица", self)
        layout_groupbox = QVBoxLayout(group_box)
        count = self.content.count_matrix
        for i in range(count):
            self._build_matrix(i, layout_groupbox, h, w)
        self._build_matrix_control_panel(layout_groupbox)
        self.layout_SArea.addWidget(group_box)

    def _build_matrix(self, i, layout_groupbox, h, w):
        """Строит каждую матрицу согласно ее номеру в сетке."""
        layout_groupbox.addWidget(QLabel(f"Матрица {i+1}"))
        self.text_fields_array.append([])
        for j in range(h):
            height_layout = QHBoxLayout()
            self._build_cell_matrix(i, j, height_layout, w)
            layout_groupbox.addLayout(height_layout)

    def _build_cell_matrix(self, i, j, height_layout, w):
        """Рисует ячейки для каждой из матрицы согласно ее размерности."""
        self.text_fields_array[i].append([])
        for k in range(w):
            text_field = QSpinBox()
            text_field.setValue(k)
            self.text_fields_array[i][j].append(text_field)
            height_layout.addWidget(text_field)

    def _build_matrix_control_panel(self, layout_groupbox):
        """Строит панель управления для перестройки матриц и вычисления
        математики, привязывая функции к кнопкам Для расширения матрицы
        передаются параметры размерности Для вычисления математики передается
        виджет для ответа."""
        size_box = QHBoxLayout()
        height_matrix = QTextEdit()
        height_matrix.setPlaceholderText("Строк")
        height_matrix.setMaximumSize(height_matrix.width(), 24)
        size_box.addWidget(height_matrix)
        width_matrix = QTextEdit()
        width_matrix.setPlaceholderText("Столбцов")
        width_matrix.setMaximumSize(width_matrix.width(), 24)
        size_box.addWidget(width_matrix)
        layout_groupbox.addLayout(size_box)
        add_size = QPushButton("Расширить")
        add_size.clicked.connect(
            partial(self._activate_connect, height_matrix, width_matrix)
        )
        layout_groupbox.addWidget(add_size)
        answer = QLabel()
        answer.setAlignment(Qt.AlignCenter)
        layout_groupbox.addWidget(answer)
        exec_example = QPushButton("Выполнить операцию")
        exec_example.clicked.connect(partial(self._execute_example, answer))
        layout_groupbox.addWidget(exec_example)

    def _activate_connect(self, h, w):
        """Активирует соединение для расширения матрицы с помощью функции
        перестройки сетки матриц."""
        height = int(h) if ((h := h.toPlainText()).isdigit()) and int(h) > 0 else False
        width = int(w) if ((w := w.toPlainText()).isdigit()) and int(w) > 0 else False
        if not height or not width:
            show_input_value_error(
                "Значение 'Строк' или 'Столбцов' должно содержать число."
            )
            return
        if height and width:
            self._build_content_matrix(height, width)
        else:
            self._build_content_matrix()

    def _execute_example(self, layout_groupbox):
        """Выполняет математические вычисления для каждого из примеров
        передавая необходимые параметры в класс построения матриц."""
        self.matrix_builder.entry_point_builder(
            parent="layout_groupbox",
            content=self.content,
            widgets=self.text_fields_array,
            layout_groupbox=layout_groupbox,
        )

    def _build_content_geometry(self):
        """Строитель контента для раздела геометрии при переключении."""
        group_box = QGroupBox("График:", self)
        group_box.setMinimumSize(500, 800)
        layout_groupbox = QVBoxLayout(group_box)
        self.__builder_canvas(group_box, layout_groupbox)
        self.__builder_text_fields(layout_groupbox)
        self.layout_SArea.addWidget(group_box)
        self.__introduce_content(self.content.example_theory)

    def __builder_canvas(self, group_box, layout_groupbox):
        self.canvas = MplCanvas(
            parent=group_box,
            dpi=80,
            td=self.content.dimensional,
        )
        graphic_layout = QHBoxLayout()
        graphic_layout.addWidget(self.canvas)
        layout_groupbox.addLayout(graphic_layout)
        layout_groupbox.addWidget(self.canvas.create_toolbar())
        self.canvas.axes.cla()
        self.canvas.axes.grid()
        graphic_btn = QPushButton("Построить график")
        graphic_btn.clicked.connect(self.__plot_builder)
        layout_groupbox.addWidget(graphic_btn)
        reset_btn = QPushButton("Очистить")
        reset_btn.clicked.connect(self.__undo_to_last_plot)
        layout_groupbox.addWidget(reset_btn)

    def __builder_text_fields(self, layout_groupbox):
        for keys_arg, default_value in self.content.args.items():
            text_edit = QTextEdit()
            text_edit.setFixedHeight(24)
            text_edit.setObjectName(keys_arg)
            text_edit.setPlaceholderText(f"{keys_arg}={default_value}")
            self.text_fields_array.append(text_edit)
            layout_groupbox.addWidget(text_edit)

    def __plot_builder(self):
        """Строитель самого графика при активации кнопки построения."""
        try:
            __args = self.content.args
            for text_field in self.text_fields_array:
                if text_value := text_field.toPlainText():
                    try:
                        value = float(text_value)
                    except ValueError:
                        show_input_value_error("Все параметры должны быть числами.")
                        for tf in self.text_fields_array:
                            tf.clear()
                        return
                    else:
                        text_field_object_name = text_field.objectName()
                        __args[text_field_object_name] = value
                        text_field.setPlaceholderText(
                            f"{text_field_object_name}={value}"
                        )

            self.graphic_builder.entry_point_builder(
                parent="axes",
                content=self.content,
                axes=self.canvas.axes,
                **__args,
            )

            self.canvas.draw()
        except Exception as e:
            print(e)

    def __clear_box(self, layout=None):
        """Очищение контента для загрузки новых данных Имитиирует механику
        работы Single Page Application (Одно окно приложения для всего проекта)
        для перезаполнения контента не ломая общую структуру окна
        приложения."""
        if not layout:
            layout = self.layout_SArea
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.__clear_box(item.layout())

    def __undo_to_last_plot(self):
        """Очищает сетку и рисует последний график при очищении полотна."""
        self.canvas.axes.cla()
        self.canvas.axes.grid()
        self.__plot_builder()

    def closeEvent(self, event):
        """Уточняет, уверен ли пользователь в желании закрыть окно
        приложения."""
        close = QMessageBox.question(
            self,
            "Выйти",
            "Вы действительно хотите закрыть приложение?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if close == QMessageBox.Yes:
            self.__clear_box(self.layout_SArea)
            event.accept()
        else:
            event.ignore()
