from dataclasses import dataclass

from pyrigami.units import MeasurementUnit, Mm


@dataclass
class Paper:
    width: MeasurementUnit
    height: MeasurementUnit

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._short_side, self._long_side = tuple(sorted((width, height)))

    def portrait(self):
        return Paper(width=self._short_side, height=self._long_side)

    def landscape(self):
        return Paper(width=self._long_side, height=self._short_side)


A4 = Paper(Mm(210), Mm(297))
