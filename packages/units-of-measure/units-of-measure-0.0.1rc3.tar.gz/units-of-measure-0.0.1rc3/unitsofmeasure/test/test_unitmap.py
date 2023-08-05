"""Test UnitMap"""
from unitsofmeasure import get_unit, map_to_unit, set_unit, Unit, UnitMap

def test() -> None:
    # not all objects are weakly referencable, but class instances are
    # https://docs.python.org/3/library/weakref.html
    class Measure:
        def __init__(self, value: object) -> None:
            self.value = value
    measure = Measure(10)
    b = Unit("b", "bit")
    units = UnitMap[Unit]()
    units.set(measure, b)
    unit = units.get(measure)
    assert unit == b

def test_decorator() -> None:
    b = Unit("b", "bit")

    @map_to_unit(b)
    def func() -> int:
        return 10

    unit = get_unit(func)
    assert unit == b

def test_set_unit() -> None:
    class Measure:
        def __init__(self, value: object) -> None:
            self.value = value
    measure = Measure(10)
    B = Unit("B", "byte")
    set_unit(measure, B)
    unit = get_unit(measure)
    assert unit == B
