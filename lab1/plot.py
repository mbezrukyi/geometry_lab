from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


@dataclass
class Data:
    a: float
    b: float
    c: int


class Function:
    def __init__(self, data: Data, f: Callable[[float], float]):
        self._data = data
        self._f = f

        self.xs = self._generate_xs()
        self.ys = self._calculate_ys()

    def _generate_xs(self) -> List[float]:
        step = abs(self._data.a - self._data.b) / self._data.c

        temp = self._data.a
        xs = []

        while self._data.b > temp:
            xs.append(round(temp, 3))
            temp += step

        return xs

    def _calculate_ys(self) -> List[float]:
        return list(map(self._f, self.xs))


class Calculator(ABC):
    def __init__(self, function: Function):
        self.function = function

    def sum_x(self, exponent: int = 1) -> float:
        return sum([
            x ** exponent
            for x in self.function.xs
        ])

    def sum_y(self) -> float:
        return sum(self.function.ys)

    def sum_x_y(self) -> float:
        return sum([
            x * y
            for x, y in zip(self.function.xs, self.function.ys)
        ])

    def sum_x_2_y(self) -> float:
        return sum([
            x ** 2 * y
            for x, y in zip(self.function.xs, self.function.ys)
        ])

    @abstractmethod
    def calculate(self) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    def find(self, x: float) -> float:
        raise NotImplementedError


class LinearCalculator(Calculator):
    def __init__(self, function: Function):
        super().__init__(function)

        self.a0, self.a1 = self._calculate_coefficients()

    def _calculate_coefficients(self) -> List[float]:
        X = np.array([
            [len(self.function.xs), self.sum_x()],
            [self.sum_x(), self.sum_x(2)]
        ])

        b = np.array([
            self.sum_y(),
            self.sum_x_y()
        ])

        coefficients = np.linalg.solve(X, b)

        return list(coefficients)

    def calculate(self) -> List[float]:
        return [
            self.find(x)
            for x in self.function.xs
        ]

    def find(self, x: float) -> float:
        return self.a0 + self.a1 * x


class QuadraticCalculator(Calculator):
    def __init__(self, function: Function):
        super().__init__(function)

        self.a0, self.a1, self.a2 = self._calculate_coefficients()

    def _calculate_coefficients(self) -> List[float]:
        X = np.array([
            [len(self.function.xs), self.sum_x(), self.sum_x(2)],
            [self.sum_x(), self.sum_x(2), self.sum_x(3)],
            [self.sum_x(2), self.sum_x(3), self.sum_x(4)]
        ])

        b = np.array([
            self.sum_y(),
            self.sum_x_y(),
            self.sum_x_2_y()
        ])

        coefficients = np.linalg.solve(X, b)

        return list(coefficients)

    def calculate(self) -> List[float]:
        return [
            self.find(x)
            for x in self.function.xs
        ]

    def find(self, x: float) -> float:
        return self.a0 + self.a1 * x + self.a2 * x ** 2


class Plot(FigureCanvas):
    def __init__(self):
        self._figure = Figure(figsize=(8, 5), dpi=100)
        self._ax = self._figure.add_subplot(111)

        super().__init__(self._figure)

    def plot(self, xs: List[float], ys: List[float], *calculators: Calculator) -> None:
        self.clear()

        self._ax.set_title('tg(x) + e^(2x)')

        self._ax.scatter(xs, ys)

        for calculator in calculators:
            self._ax.plot(calculator.function.xs, calculator.calculate())

        self.draw()

    def clear(self) -> None:
        self._ax.clear()
        self.draw()
