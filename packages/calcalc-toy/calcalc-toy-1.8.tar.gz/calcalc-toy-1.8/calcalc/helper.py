import numexpr as ne
from urllib.request import urlopen
from urllib.parse import quote
import json
import sys


def calculate_locally(s):
    answer = float(ne.evaluate(s))
    return answer


def calculate_remotely(s, return_float=True):
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
