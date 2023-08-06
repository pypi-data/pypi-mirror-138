
# Import Modules
from calcalc.CalCalc import calculate
import math


# Is my output a float?
def test_output_type():
    isinstance(calculate("2**2"), float) == True


# Is my output numerically accurate?
def test_output_accurate():
    assert (4.0 - calculate("2**2")) < 0.0001


# Can Wolfram do math?
def test_wolfram():
    assert (4.0 - calculate("Two plus Two")) < 0.0001


# Can wolfram recall well-known, highly significant numerical values?
def test_wolf_num():
    assert calculate('What is the flight velocity of a sparrow?') == 25.0


# Can I pull string answers from Wolfram?
def test_wolf_string():
    assert calculate('Hello') == 'Hello, human.'


# Can the code handles nonsense?
def test_nonsense():
    assert math.isnan(calculate('rawr')) == True
