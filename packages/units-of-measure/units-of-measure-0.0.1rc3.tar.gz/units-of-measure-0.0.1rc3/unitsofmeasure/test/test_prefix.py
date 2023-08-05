"""Test Prefix"""
import pytest
from unitsofmeasure import Prefix, PREFIX_1

@pytest.mark.parametrize(
    "base , exponent , symbol , name"  ,[
    (  10 ,        0 , ""     , ""     ),
    (  10 ,        1 , "da"   , "deca" ), # SI prefixes (decimal)
    (  10 ,        2 , "h"    , "hecto"),
    (  10 ,        3 , "k"    , "kilo" ),
    (  10 ,        6 , "M"    , "mega" ),
    (  10 ,        9 , "G"    , "giga" ),
    (  10 ,       12 , "T"    , "tera" ),
    (  10 ,       15 , "P"    , "peta" ),
    (  10 ,       18 , "E"    , "exa"  ),
    (  10 ,       21 , "Z"    , "zetta"),
    (  10 ,       24 , "Y"    , "yotta"),
    (  10 ,       -1 , "d"    , "deci" ),
    (  10 ,       -2 , "c"    , "centi"),
    (  10 ,       -3 , "m"    , "milli"),
    (  10 ,       -6 , "µ"    , "micro"),
    (  10 ,       -9 , "n"    , "nano" ),
    (  10 ,      -12 , "p"    , "pico" ),
    (  10 ,      -15 , "f"    , "femto"),
    (  10 ,      -18 , "a"    , "atto" ),
    (  10 ,      -21 , "z"    , "zepto"),
    (  10 ,      -24 , "y"    , "yocto")
])
def test_prefix(base: int, exponent: int, symbol: str, name: str) -> None:
    prefix = Prefix(base=base, exponent=exponent, symbol=symbol, name=name)
    assert prefix.base     == base
    assert prefix.exponent == exponent
    assert prefix.symbol   == symbol
    assert prefix.name     == name

def test_prefix_1() -> None:
    assert PREFIX_1.base        == 10
    assert PREFIX_1.exponent    == 0
    assert len(PREFIX_1.symbol) == 0
    assert len(PREFIX_1.name)   == 0
