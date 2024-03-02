from typing import Any

from PyQt5.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .plot import Data, Function, LinearCalculator, QuadraticCalculator
from .scene import Scene
from .utils import custom_function, read_json


class Field(QWidget):
    def __init__(self, name: str):
        super().__init__()

        self._layout = QHBoxLayout()

        self._label = QLabel(name)
        self._line_edit = QLineEdit()

        self._init_ui()

    def _init_ui(self) -> None:
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._line_edit)

        self.setLayout(self._layout)

    def set_value(self, value: Any) -> None:
        self._line_edit.setText(str(value))

    def get_value(self) -> Any:
        return self._line_edit.text()


class PointResult(QWidget):
    def __init__(self, name: str):
        super().__init__()

        self._layout = QHBoxLayout()

        self._label = QLabel(name)
        self._result = QLabel()

        self._init_ui()

    def _init_ui(self) -> None:
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._result)

        self.setLayout(self._layout)

    def set_result(self, value: float) -> None:
        self._result.setText(str(value))


class DataFulfillmentSettings(QGroupBox):
    def __init__(self, data_file_name: str, graphics_scene: Scene, *fields: Field):
        super().__init__()

        self._data_file_name = data_file_name
        self._graphics_scene = graphics_scene

        self._layout = QVBoxLayout()

        self._a_field, self._b_field, self._c_field = fields

        self._apply_button = QPushButton('Apply')
        self._read_file_button = QPushButton('Load data')

        self._init_ui()

    def _init_ui(self) -> None:
        self._apply_button.clicked.connect(self._apply)
        self._read_file_button.clicked.connect(self._load_data)

        self._layout.addWidget(self._a_field)
        self._layout.addWidget(self._b_field)
        self._layout.addWidget(self._c_field)
        self._layout.addWidget(self._apply_button)
        self._layout.addWidget(self._read_file_button)

        self.setLayout(self._layout)

    def _apply(self) -> None:
        a = float(self._a_field.get_value())
        b = float(self._b_field.get_value())
        c = int(self._c_field.get_value())

        data = Data(a, b, c)

        sin_function = Function(data, custom_function)

        linear_calculator = LinearCalculator(sin_function)
        quadratic_calculator = QuadraticCalculator(sin_function)

        self._graphics_scene.draw(
            sin_function.xs,
            sin_function.ys,
            linear_calculator,
            quadratic_calculator
        )

    def _load_data(self) -> None:
        json_data = read_json(self._data_file_name)

        data = Data(
            a=json_data.get('A'),
            b=json_data.get('B'),
            c=json_data.get('C')
        )

        self._a_field.set_value(data.a)
        self._b_field.set_value(data.b)
        self._c_field.set_value(data.c)

        sin_function = Function(data, custom_function)

        print(sin_function.xs)
        print(sin_function.ys)

        linear_calculator = LinearCalculator(sin_function)
        quadratic_calculator = QuadraticCalculator(sin_function)

        self._graphics_scene.draw(
            sin_function.xs,
            sin_function.ys,
            linear_calculator,
            quadratic_calculator
        )


class CurveVisibilitySettings(QGroupBox):
    def __init__(self, graphics_scene: Scene, *fields: Field):
        super().__init__()

        self._graphics_scene = graphics_scene

        self._a_field, self._b_field, self._c_field = fields

        self._layout = QVBoxLayout()

        self._linear_check_box = QCheckBox('Linear')
        self._quadratic_check_box = QCheckBox('Quadratic')

        self._init_ui()

    def _init_ui(self) -> None:
        self._linear_check_box.setChecked(True)
        self._quadratic_check_box.setChecked(True)

        self._linear_check_box.stateChanged.connect(self._check_box_state_changed)
        self._quadratic_check_box.stateChanged.connect(self._check_box_state_changed)

        self._layout.addWidget(self._linear_check_box)
        self._layout.addWidget(self._quadratic_check_box)

        self.setLayout(self._layout)

    def _check_box_state_changed(self) -> None:
        a = float(self._a_field.get_value())
        b = float(self._b_field.get_value())
        c = int(self._c_field.get_value())

        data = Data(a, b, c)

        sin_function = Function(data, custom_function)

        calculators = []

        if self._linear_check_box.isChecked():
            calculators.append(LinearCalculator(sin_function))
        if self._quadratic_check_box.isChecked():
            calculators.append(QuadraticCalculator(sin_function))

        self._graphics_scene.draw(
            sin_function.xs,
            sin_function.ys,
            *calculators
        )


class PointSettings(QGroupBox):
    def __init__(self, *fields: Field):
        super().__init__()

        self._a_field, self._b_field, self._c_field = fields

        self._layout = QVBoxLayout()

        self._x_field = Field('X:')

        self._y_linear_result = PointResult('Y Linear:')
        self._y_quadratic_result = PointResult('Y Quadratic:')

        self._apply_button = QPushButton('Apply')

        self._init_ui()

    def _init_ui(self) -> None:
        self._apply_button.clicked.connect(self._apply)

        self._layout.addWidget(self._x_field)
        self._layout.addWidget(self._y_linear_result)
        self._layout.addWidget(self._y_quadratic_result)
        self._layout.addWidget(self._apply_button)

        self.setLayout(self._layout)

    def _apply(self) -> None:
        a = float(self._a_field.get_value())
        b = float(self._b_field.get_value())
        c = int(self._c_field.get_value())

        data = Data(a, b, c)

        sin_function = Function(data, custom_function)

        linear_calculator = LinearCalculator(sin_function)
        quadratic_calculator = QuadraticCalculator(sin_function)

        x = float(self._x_field.get_value())

        y_linear_result = linear_calculator.find(x)
        y_quadratic_result = quadratic_calculator.find(x)

        self._y_linear_result.set_result(y_linear_result)
        self._y_quadratic_result.set_result(y_quadratic_result)


class SettingsPanel(QWidget):
    def __init__(self, data_file_name: str, graphics_scene: Scene, min_width: int = 300):
        super().__init__()

        self._min_width = min_width

        self._layout = QVBoxLayout()

        self._graphics_scene = graphics_scene

        fields = [
            Field('A:'),
            Field('B:'),
            Field('C:')
        ]

        self._data_fulfillment_settings = DataFulfillmentSettings(
            data_file_name,
            self._graphics_scene,
            *fields
        )
        self._curve_visibility_settings = CurveVisibilitySettings(self._graphics_scene, *fields)
        self._point_settings = PointSettings(*fields)

        self._clear_button = QPushButton('Clear')

        self._init_ui()

    def _init_ui(self) -> None:
        self.setMinimumWidth(self._min_width)

        self._clear_button.clicked.connect(self._clear)

        self._layout.addWidget(self._data_fulfillment_settings)
        self._layout.addWidget(self._curve_visibility_settings)
        self._layout.addWidget(self._point_settings)
        self._layout.addWidget(self._clear_button)

        self.setLayout(self._layout)

    def _clear(self) -> None:
        self._graphics_scene.clear()
