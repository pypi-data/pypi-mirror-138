"""Test Unit"""
import pytest
from fractions import Fraction
from unitsofmeasure import decprefix, Dimension, Prefix, PREFIX_1, SCALAR, Unit, UNIT_1

@pytest.mark.parametrize(
    "symbol , name       , dimension        , prefix,     , factor",[
    ("%"    , "percent"  , Dimension()      , PREFIX_1   , Fraction(1,100)), # scalar
    ("kg"   , "kilogram" , Dimension(kg=1)  , decprefix.k , Unit.FRACTION_1), # SI base units
    ("m"    , "metre"    , Dimension(m=1)   , PREFIX_1   , Unit.FRACTION_1),
    ("s"    , "second"   , Dimension(s=1)   , PREFIX_1   , Unit.FRACTION_1),
    ("A"    , "ampere"   , Dimension(A=1)   , PREFIX_1   , Unit.FRACTION_1),
    ("K"    , "kelvin"   , Dimension(K=1)   , PREFIX_1   , Unit.FRACTION_1),
    ("cd"   , "candela"  , Dimension(cd=1)  , PREFIX_1   , Unit.FRACTION_1),
    ("mol"  , "mole"     , Dimension(mol=1) , PREFIX_1   , Unit.FRACTION_1)
])
def test_unit(symbol: str, name: str, dimension: Dimension, prefix: Prefix, factor: Fraction) -> None:
    unit = Unit(symbol, name, dimension, prefix, factor)
    assert unit.symbol    == symbol
    assert unit.name      == name
    assert unit.dimension == dimension
    assert unit.prefix    == prefix
    assert unit.factor    == factor

def test_no_unit() -> None:
    assert len(UNIT_1.symbol) == 0
    assert len(UNIT_1.name)   == 0
    assert UNIT_1.dimension   == SCALAR
    assert UNIT_1.prefix      == PREFIX_1
    assert UNIT_1.factor      == Unit.FRACTION_1
