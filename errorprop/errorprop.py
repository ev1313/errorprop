import sympy as sy
import numpy as np
import uncertainties as uc

"""
    Parameters
    ==========
    equation : string
        symbol string to be used in equation, needs to be sympy syntax (I is imaginary unit for example)
    datadict: dictionary
        the keys of this dictionary represent the symbols used in the equation string.
        each key can either be a 2-tuple or a list of 2-tuples or 3-tuples.

        a 2-tuple consists of the value and the error/deviation. (the error can be 0 if none is necessary)
        the same goes for the elements of a list.

        if lists are used, all need to be of the same length!
"""
def calc_errorprop(equation, datadict):
    eq_expr = sy.sympify(equation)
    err_expr = 0
    calc = {}
    data_list_len = 0
    for n, data in datadict.items():
        if isinstance(data, tuple):
            assert(len(data)==2, "{} tuple does not have two elements!".format(n))

        elif isinstance(data, list):
            if not data_list_len == 0:
                data_list_len = len(data)
            else:
                assert(data_list_len == len(data), "data lists have inconsistent lengths! {} has length {} but should have {}".format(n, len(data), data_list_len))

            i = 0
            for d in data:
                assert(isinstance(d, tuple), "data list {} {} contains not a tuple at position {}!".format(d,i))
                assert(len(d)==2, "{} tuple in data list at position {} does not have two elements!".format(n, d, i))
                i+=1

        else:
            assert(False, "{} data is not tuple or list!".format(n))
            
        # generate derivates
        symbol = sy.Symbol(n)
        symbol_err = sy.Symbol("sigma_{}".format(n))
        symbol_der = sy.diff(eq_expr,symbol)
        symbol_der = symbol_der * symbol_err 

        calc[n] = (symbol, symbol_der, symbol_err)
        err_expr = err_expr + symbol_der**2

    err_expr = sy.simplify(sy.sqrt(err_expr))
    err_expr = sy.powdenest(err_expr, force=True)

    nominal = eq_expr
    deviation = err_expr

    # calculate nominal + deviate values
    for n, d in datadict.items():
        nominal = nominal.subs(calc[n][0], str(d[0]))
        deviation = deviation.subs(calc[n][0], str(d[0]))
        deviation = deviation.subs(calc[n][2], str(d[1]))

    try:
        nominal = float(nominal)
    except:
        assert(False, "Could not finish nominal evalution due to missing values, stopped with equation {}".format(str(nominal)))
        
    try:
        deviation = float(deviation)
    except:
        assert(False, "Could not finish deviation evalution due to missing values, stopped with equation {}".format(str(deviation)))

    # cast to uncertainties
    return uc.ufloat(nominal,deviation)

