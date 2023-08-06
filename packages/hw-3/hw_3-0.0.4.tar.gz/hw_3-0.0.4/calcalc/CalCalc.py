# the same as before, but this time the file is written in calcalc\CalCalc.py
import urllib.parse
import requests
import argparse
# from unittest import TestCase

def calculate(my_para_string, return_float=True):
    if not my_para_string.find('__') == -1:
        raise ValueError('no \'__\' allowed in string')
    try:
        my_para_string = my_para_string.replace('^','**')
        return(eval(my_para_string))
    except:
        appid = 'J27WQX-V46A6GK62E'
        query = urllib.parse.quote_plus(my_para_string)
        query_url = f"http://api.wolframalpha.com/v2/query?" \
                     f"appid={appid}" \
                     f"&input={query}" \
                     f"&format=plaintext" \
                     f"&output=json"
        r = requests.get(query_url).json()
        data = r["queryresult"]["pods"][1]["subpods"][0]
        plaintext = data["plaintext"]
        if not return_float:
            return plaintext
        else:
            plaintext = plaintext.replace('×','*')
            plaintext = plaintext.replace('^','**')
            for i in range(1,len(plaintext)):
                if plaintext[i-1] == '*' or plaintext[i-1] == '/' or plaintext[i-1] == '+' or plaintext[i-1] == '-':
                    continue
                try:
                    eval(plaintext[0:i])
                except:
                    break
            if i == 1:
                return None
            else:
                return eval(plaintext[0:i-1])

def test_1():
    assert abs(4. - calculate('2**2')) < 0.001
def test_2():
    assert abs(4. - calculate('2^2')) < 0.001
def test_3():
    assert abs(7.3459*10**22 - calculate('mass of moon in kg'))/(7.3459*10**22) < 0.001
def test_4():
    assert abs(10. - calculate('2+8')) < 0.001
def test_5():
    assert abs(6.626*10**-34. - calculate('planck constant'))/(6.626*10**-34) < 0.001
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sample Application')
    parser.add_argument('-f', action='store_false', default=True,
                    dest='floatformat',
                    help='Set float output to False')
    parser.add_argument('-w', action='store', dest='string',
                    help='String needs to be calculated')
    my_string = None
    results = parser.parse_args()
    my_string = results.string
    if my_string == None:
        raise ValueError('please input string by -w')
    
    print(calculate(my_string, results.floatformat))
