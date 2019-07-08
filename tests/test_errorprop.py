from errorprop.errorprop import calc_errorprop

import pdb

def test_errorprop1():
    datadict = {
            "m": (1., 0.1),
            "c": (28E3, 0.0)
            }
    E = calc_errorprop("m*c**2", datadict)

    print(E)
    pdb.set_trace()
