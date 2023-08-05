from dataclasses import dataclass
from enum import Enum
from functools import total_ordering


@dataclass
@total_ordering
class MeasurementUnit:
    value: float

    def __eq__(self, other):
        if not isinstance(other, MeasurementUnit):
            return NotImplemented
        return self.to_pt() == other.to_pt()

    def __lt__(self, other):
        if not isinstance(other, MeasurementUnit):
            return NotImplemented
        return self.to_pt().value < other.to_pt().value


class Consts(Enum):
    MM_PER_INCH = 25.4
    PT_PER_INCH = 72


NUMERIC_TYPES = (int, float)


class UnitArithmeticError(TypeError):
    def __init__(self):
        super().__init__(
            """Addition and Subtraction work only among fellow MeasurementUnit-s.
        A MeasurementUnit can only be multiplied/divided by a scalar."""
        )


@dataclass
class In(MeasurementUnit):
    """An Inch"""

    def to_mm(self):
        return Mm(self.value * Consts.MM_PER_INCH.value)

    def to_pt(self):
        return Pt(self.value * Consts.PT_PER_INCH.value)

    def to_in(self):
        return self

    def __add__(self, other):
        if isinstance(other, MeasurementUnit):
            return (self.to_pt() + other).to_in()
        else:
            raise UnitArithmeticError

    def __sub__(self, other):
        if isinstance(other, MeasurementUnit):
            return (self.to_pt() - other).to_in()
        else:
            raise UnitArithmeticError

    def __mul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return In(self.value * other)
        else:
            raise UnitArithmeticError

    def __truediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return In(self.value / other)
        else:
            raise UnitArithmeticError

    def __floordiv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return In(self.value // other)
        else:
            raise UnitArithmeticError


@dataclass
class Mm(MeasurementUnit):
    """A Millimeter"""

    def to_in(self):
        return In(self.value / Consts.MM_PER_INCH.value)

    def to_pt(self):
        return self.to_in().to_pt()

    def to_mm(self):
        return self

    def __add__(self, other):
        if isinstance(other, MeasurementUnit):
            return (self.to_pt() + other).to_mm()
        else:
            raise UnitArithmeticError

    def __sub__(self, other):
        if isinstance(other, MeasurementUnit):
            return (self.to_pt() - other).to_mm()
        else:
            raise UnitArithmeticError

    def __mul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Mm(self.value * other)
        else:
            raise UnitArithmeticError

    def __truediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Mm(self.value / other)
        else:
            raise UnitArithmeticError

    def __floordiv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Mm(self.value // other)
        else:
            raise UnitArithmeticError


@dataclass
class Pt(MeasurementUnit):
    """A point, 1/72th of an inch"""

    def to_in(self):
        return In(self.value / Consts.PT_PER_INCH.value)

    def to_mm(self):
        return self.to_in().to_mm()

    def to_pt(self):
        return self

    def __add__(self, other):
        if isinstance(other, MeasurementUnit):
            return Pt(self.value + other.to_pt().value)
        else:
            raise UnitArithmeticError

    def __sub__(self, other):
        if isinstance(other, MeasurementUnit):
            return Pt(self.value - other.to_pt().value)
        else:
            raise UnitArithmeticError

    def __mul__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Pt(self.value * other)
        else:
            raise UnitArithmeticError

    def __truediv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Pt(self.value / other)
        else:
            raise UnitArithmeticError

    def __floordiv__(self, other):
        if isinstance(other, NUMERIC_TYPES):
            return Pt(self.value // other)
        else:
            raise UnitArithmeticError
