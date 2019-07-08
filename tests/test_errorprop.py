from errorprop.errorprop import calc_errorprop

def test_errorprop1():
    datadict = {
            "m": (1., 0.1),
            "c": (28E3, 0.0)
            }
    E = calc_errorprop("m*c**2", datadict)
    
    assert(round(E.n,6)==7.84e8)
    assert(round(E.std_dev,6)==7.84e7)
