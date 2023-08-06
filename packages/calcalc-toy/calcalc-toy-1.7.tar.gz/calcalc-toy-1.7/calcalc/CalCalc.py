import argparse
import numexpr as ne
import numpy as np
from urllib.request import urlopen
from urllib.parse import quote
import json
import sys


def _get_input_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", action="store", dest="simple_expression", type=str,
        help="Enter a simple mathematical expression"
    )
    parser.add_argument(
        "-w", action="store", dest="for_wolfram", type=str,
        help="Enter a complex question for WolframAlpha"
    )
    parser.add_argument(
        "--float", action="store_true", dest="return_float",
        help="Return Wolfram results as float instead of text?"
    )
    args = parser.parse_args()

    if args.simple_expression is None and args.for_wolfram is None:
        raise TypeError("Specify an input with \'-s\' (simple expression)" +
                        "or \'-w\' (for WolframAlpha)")

    return args


def calculate(s, local=True, return_float=True):
    """
    This function calculates the expression either
    locally or on WolframAlpha.

    If calculate locally, set local=True.
    If calculate with Wolfram, set local=False.

    When using Wolfram, if want to display computation results
    as string, e.g. "1.4×10^2 kg (kilograms)", then set return_float=False.
    Otherwise, set return_float=True to convert it to float.
    """
    if local:
        try:
            return _calculate_locally(s)
        except:
            print('NOTE: Not a valid numerical expression!!! \n'
                  'Please switch to WolframAlpha using local=False! \n')
    else:
        return _calculate_remotely(s, return_float=return_float)


def _calculate_locally(s):
    answer = float(ne.evaluate(s))
    return answer


def _calculate_remotely(s, return_float=True):
    url = _use_wolfram(s)
    answer_raw = _get_result_from_wolfram(url)
    answer = _convert_result_from_wolfram(answer_raw,
                                          return_float=return_float)

    if answer is None:
        sys.exit('NOTE: Invalid question for'
                 'Wolfram to return a single number!')

    return answer


def _use_wolfram(s):
    s = quote(s)
    SERVICE = 'http://api.wolframalpha.com/v2/query?appid='
    ID = '5TG54Y-K3JUTT44Y8'
    INPUT = '&input=' + s
    url = SERVICE + ID + INPUT + '&output=json'
    return url


def _get_result_from_wolfram(url):

    try:
        data = json.load(urlopen(url))
        pods = data['queryresult']['pods']
        for pod in pods:
            if pod['id'] == 'Result':
                answer = pod['subpods'][0]['plaintext']
                return answer
    except:
        sys.exit('NOTE: Invalid question for'
                 'Wolfram to return a single number!')


def _convert_result_from_wolfram(s, return_float=True):
    if return_float is False:
        return s
    # usually in form Ax10^B
    try:
        s = s.split()[0]
        if '×' in s or '^' in s:
            num = float(s.split('×')[0])
            expo = float(s.split('^')[-1])
            out = num * 10**expo
            return out
        else:
            return float(s)
    except:
        sys.exit('NOTE: Invalid question for'
                 'Wolfram to return a single number!')


"""
Writing my tests...
"""


def test_1():  # test local
    assert abs(2 * np.sin(3 / 5) + np.log(7)
               - calculate("2*sin(3/5)+log(7)")) < 0.001


def test_2():  # test WolframAlpha
    assert abs(7.3459e+23 - calculate('mass of the moon in kg',
               return_float=True, local=False) * 10) < 0.001


def test_3():  # simple expression, but use WolframAlpha
    assert abs(6.0 - calculate('2*3',
               return_float=True, local=False)) < 0.001


def test_4():  # test WolframAlpha, string output
    assert calculate('mass of the moon in kg',
                     return_float=False, local=False) \
                     == '7.3459×10^22 kg (kilograms)'


def test_5():  # test WolframAlpha result conversion
    assert _convert_result_from_wolfram('-123.5') == -123.5
    assert _convert_result_from_wolfram('1.3×10^5') == 1.3*10**5
    assert _convert_result_from_wolfram('1') == 1


if __name__ == "__main__":

    args = _get_input_args()

    if args.simple_expression:
        print(calculate(args.simple_expression))

    if args.for_wolfram:
        print(calculate(args.for_wolfram, local=False,
                        return_float=args.return_float))
