"""Test Dimension"""
import pytest
from unitsofmeasure import Dimension, SCALAR

@pytest.mark.parametrize(
    "dimension        , kg , m , s , A , K , cd , mol",[
    (Dimension()      ,  0 , 0 , 0 , 0 , 0 ,  0 ,   0), # scalar
    (Dimension(kg=1)  ,  1 , 0 , 0 , 0 , 0 ,  0 ,   0), # SI base units
    (Dimension(m=1)   ,  0 , 1 , 0 , 0 , 0 ,  0 ,   0),
    (Dimension(s=1)   ,  0 , 0 , 1 , 0 , 0 ,  0 ,   0),
    (Dimension(A=1)   ,  0 , 0 , 0 , 1 , 0 ,  0 ,   0),
    (Dimension(K=1)   ,  0 , 0 , 0 , 0 , 1 ,  0 ,   0),
    (Dimension(cd=1)  ,  0 , 0 , 0 , 0 , 0 ,  1 ,   0),
    (Dimension(mol=1) ,  0 , 0 , 0 , 0 , 0 ,  0 ,   1)
])
def test_dimension(dimension: Dimension, kg: int, m: int, s: int, A: int, K: int, cd: int, mol: int) -> None:
    assert dimension.kg  == kg
    assert dimension.m   == m
    assert dimension.s   == s
    assert dimension.A   == A
    assert dimension.K   == K
    assert dimension.cd  == cd
    assert dimension.mol == mol

def test_scalar() -> None:
    assert SCALAR.kg  == 0
    assert SCALAR.m   == 0
    assert SCALAR.s   == 0
    assert SCALAR.A   == 0
    assert SCALAR.K   == 0
    assert SCALAR.cd  == 0
    assert SCALAR.mol == 0
