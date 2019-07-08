import pytest

from errorprop.errorprop import calc_gaussian_errorprop_single, calc_gaussian_errorprop_multi
import sympy as sy

def test_errorprop_single_simple():
    datadict = {
            "m": (1., 0.1),
            "c": (28E3, 0.0)
            }
    E = calc_gaussian_errorprop_single(sy.sympify("m*c**2"), datadict)

    assert(len(E)==2)
    assert(round(E[0],6)==7.84e8)
    assert(round(E[1],6)==7.84e7)

def test_errorprop_single_assert_type():
    with pytest.raises(Exception):
        datadict = {
            "m": "Abc",
            "c": 1.0
        }
        E = calc_gaussian_errorprop_single(sy.sympify("m*c**2"), datadict)

def test_errorprop_multi_simple():
    datadict = {
            "m": [
                (1., 0.1),
                (2., 0.01),
                (3., 0.15),
                (4., 0.0),
            ],
            "c": (28E3, 0.0)
            }
    E = calc_gaussian_errorprop_multi(sy.sympify("m*c**2"), datadict)

    assert(len(E)==4)
    assert(round(E[0][0], 5) == 784000000.000000)
    assert(round(E[1][0], 5) == 1568000000.00000)
    assert(round(E[2][0], 5) == 2352000000.00000)
    assert(round(E[3][0], 5) == 3136000000.00000)
    assert(round(E[0][1], 5) == 78400000.0000000)
    assert(round(E[1][1], 5) == 7840000.00000000)
    assert(round(E[2][1], 5) == 117600000.000000)
    assert(round(E[3][1], 5) == 0)

def test_errorprop_multi_no_lists():
    datadict = {
            "m": (1., 0.1),
            "c": (28E3, 0.0)
            }
    E = calc_gaussian_errorprop_multi(sy.sympify("m*c**2"), datadict)

    assert(len(E)==1)
    assert(round(E[0][0],6)==7.84e8)
    assert(round(E[0][1],6)==7.84e7)
