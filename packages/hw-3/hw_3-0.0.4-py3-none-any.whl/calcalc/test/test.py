import urllib.parse
import requests
import argparse
import calcalc
# from unittest import TestCase


def test_1():
    assert abs(4. - calcalc.CalCalc.calculate('2**2')) < 0.001
def test_2():
    assert abs(4. - calcalc.CalCalc.calculate('2^2')) < 0.001
def test_3():
    assert abs(7.3459*10**22 - calcalc.CalCalc.calculate('mass of moon in kg'))/(7.3459*10**22) < 0.001
def test_4():
    assert abs(10. - calcalc.CalCalc.calculate('2+8')) < 0.001
def test_5():
    assert abs(6.626*10**-34. - calcalc.CalCalc.calculate('planck constant'))/(6.626*10**-34) < 0.001