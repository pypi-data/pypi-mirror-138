# Note to self: hash-tags above a magic function are a no, no in Python.

# Import Modules
import urllib.request as request
import argparse
import numexpr as ne

# In order to get urllib.request to work from the command line,
# you HAVE to import it specifically, as above.
#
# When Calcalc.py is used from the command line,
# import urllib didn't actuallyimport everything, and I kept
# getting a AttributeError: module urllib has no attribute 'request.'


# Define a function (which will go into calculate) for accessing Wolfram Alpha.
def ask_wolfram(input_string):
    """
    Inputs
    ----------
    input_string: str
        A string to be passed to Wolfram Alpha.

    Output
    ----------
    answer_as_text: float
        The result from Wolfram Alpha, expressed as a float.
    """

    # put together query address
    url_prefix = "http://api.wolframalpha.com/v2/query?input="
    query = input_string
    query_nice = query.replace("+", "%2B").replace(
        " ", "+"
    )  # replace numeric '+' symbols; make '+' = space;
    query_opt = "&appid=6A8HR8-JR3LAA5QAT&format=plaintext&includepodid=Result"

    # decode utf-8 to text.
    full_url = url_prefix + query_nice + query_opt
    f = request.urlopen(full_url)
    f_as_text = f.read().decode("utf-8")
    # print(f_as_text)

    # pull out answer from plaintext section of query output
    idx_0 = f_as_text.find("<plaintext>") + 11
    idx_stop = f_as_text.find("</plaintext>", idx_0)
    # print(f_as_text[idx_0:idx_stop])

    # turn the first result into a number
    try:
        num = f_as_text[idx_0:idx_stop].split(" ")[0]
        answer = ne.evaluate(num.replace("×", "*").replace("^", "**")) + 0.0
        return answer

        # What if the result isn't a number at all?
    except (KeyError, TypeError):
        answer = f_as_text[idx_0:idx_stop]
        return answer


# Define function to evaluate an input string with numexpr.
def calculate(input_string):
    """
    Inputs
    ----------
    input_string: str
        A string to be passed to numexpr.evaluate.

    Output
    ----------
    answer: float
        The result of numexpr.evaluate(string), expressed as a float.
    """

    # Check that the string is actually a str.
    if type(input_string) != str:
        raise ValueError("The input isn't a string. Check input syntax")

    # Evaluate input_string with numexpr.evaluate
    try:
        answer = ne.evaluate(input_string) + 0.0
        answer.astype(float)
        return answer
    except (KeyError, SyntaxError):
        print(f'Could not evaluate \'{input_string}\'. Trying Wolfram Alpha')

        # Run wolfram alpha if numexpr can't solve it!
        try:
            answer = ask_wolfram(input_string)
            return answer
        except (ValueError, SyntaxError):
            print("Wolfram could not solve the query. Returning NaN.")
            answer = float("nan")
            return answer


# Parse command line arguments (when using from command line)
# Hash this out if you just want to test individual functions
# in the Jupyter Notebook.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcalc - calculate")
    parser.add_argument(
        "input_string",
        help="Input string to be evaluated. Required positional argument.",
    )
    answer = parser.parse_args()

    # Execute Function!
    print(calculate(answer.input_string))