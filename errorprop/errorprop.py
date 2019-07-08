import sympy as sy
import numpy as np

"""
    This method calculates the given equation and does a gaussian error propagation for a single datapoint.

    Parameters
    ==========
    equation : string
        symbol string to be used in equation, needs to be sympy syntax (I is imaginary unit for example)
    datadict: dictionary
        the keys of this dictionary represent the symbols used in the equation string.
        each key has to be a 2-tuple in the format (value, deviation)
"""
def calc_gaussian_errorprop_single(equation, datadict):
    err_expr = 0
    calc = {}
    for n, data in datadict.items():
        if isinstance(data, tuple):
            if not len(data)==2:
                raise ValueError("{} tuple does not have two elements!".format(n))
        else:
            raise ValueError("{} data is not a 2-tuple!".format(n))
        # generate derivates
        symbol = sy.Symbol(n)
        symbol_err = sy.Symbol("sigma_{}".format(n))
        symbol_der = sy.diff(equation,symbol)
        symbol_der = symbol_der * symbol_err

        calc[n] = (symbol, symbol_der, symbol_err)
        err_expr = err_expr + symbol_der**2

    err_expr = sy.simplify(sy.sqrt(err_expr))
    err_expr = sy.powdenest(err_expr, force=True)

    nominal = equation
    deviation = err_expr

    # calculate nominal + deviate values
    for n, d in datadict.items():
        nominal = nominal.subs(calc[n][0], str(d[0]))
        deviation = deviation.subs(calc[n][0], str(d[0]))
        deviation = deviation.subs(calc[n][2], str(d[1]))

    return nominal, deviation

"""
    This method calculates a gaussian error propagation similar to calc_gaussian_errorprop_single, however allows lists in the datadict also.

    Parameters
    ==========
    equation : sympy equation
        the equation to be used
    datadict: dictionary
        the keys of this dictionary represent the symbols used in the equation string.
        each key has to be a 2-tuple or a list of 2-tuples all in the format (value, deviation)

        all lists in the datadict have to have the same length.

    Returns
    =======
        a list with the length of the lists in the datadict is returned.
"""
def calc_gaussian_errorprop_multi(equation, datadict):
    results = []
    data_list_len = 0
    for n, data in datadict.items():
        if isinstance(data, list):
            if not len(data):
                raise ValueError("{} contains an empty list!".format(n))
            if not data_list_len:
                data_list_len = len(data)
            else:
                if not data_list_len == len(data):
                    raise ValueError("data lists have inconsistent lengths! {} has length {} but should have {}".format(n, len(data), data_list_len))

            i = 0
            for d in data:
                if not isinstance(d, tuple):
                    raise ValueError("data list {} {} contains not a tuple at position {}!".format(n, d, i))
                if not len(d)==2:
                    raise ValueError("{} tuple in data list at position {} does not have two elements!".format(n, d, i))
                i+=1
        elif isinstance(data, tuple):
            if not len(data)==2:
                raise ValueError("{} tuple does not have two elements!".format(n))
        else:
            raise ValueError("{} data is not a 2-tuple!".format(n))

    results = []

    if data_list_len == 0:
        results.append(calc_gaussian_errorprop_single(equation, datadict))
    else:
        for i in range(data_list_len):
            temp_data = {}
            for n, data in datadict.items():
                if isinstance(data, list):
                    temp_data[n] = data[i]
                else:
                    temp_data[n] = data
                    results.append(calc_gaussian_errorprop_single(equation, temp_data))

    return results
