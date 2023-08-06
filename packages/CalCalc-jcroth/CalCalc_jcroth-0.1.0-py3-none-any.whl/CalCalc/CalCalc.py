import sys
import urllib.request as req
from json import loads

_app_id = "WJ8L5W-QUPLPE642A"
_supported_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "^", "(", ")"]
_supported_wolfram_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]

# Determines if expression should be evaluated locally or on WolframAlpha
def calculate(expr, return_float=False):
    result = None

    # If characters are supported evaluation can be done locally
    if _verify_supported_chars(expr):
        # Perform evaluation, store result
        result = _eval_math(expr)
    
    # Evaluation cannot be done locally, call wolfram
    else:
        result = _wolfram(expr)

    # Cast to float if asked, catching error
    if return_float:
        try:
            return float(result)
        except ValueError:
            print("cannot convert result to a float")
    else:
        return result

# Checks if an expression only contains characters
def _verify_supported_chars(expr):
    # Ensure that expr only contains supported characters
    all_chars_supported = True
    for c in expr:
        if c not in _supported_chars:
            all_chars_supported = False

    return all_chars_supported

# Removes unsupported characters from expression returned by WolframAlpha
def _strip_unsupported_chars(expr):
    new_expr = ""
    # Loop through each character, add to new expression if character is supported
    i = 0
    while i < len(expr):
        # If character is in supported characters list, append to new_expr and iterate index by 1
        if expr[i] in _supported_wolfram_chars:
            new_expr += expr[i]
            i += 1
        # If character is "×" then scan forwards to determine if the expression is going to be in scientific notation
        elif expr[i] == "×" and i+4 < len(expr) and expr[i+1:i+4] == "10^":
            # Expression is in scientific notation, check if negative or positive exponent,  write in pythonic form, and skip "10^" or "10^-"
            if expr[i+4] == "-":
                new_expr += "e-"
                i += 4
            else:
                new_expr += "e+"
                i += 3
        # If expression contains space, break loop and return expression
        elif expr[i] == " ":
            break
        # If none of the above, iterate loop without updating new_expr
        else:
            i += 1

    return new_expr

# Evaluates math expression locally
def _eval_math(expr):

    # Replace ^ with ** so that python doesn't get confused
    new_expr = expr.replace("^", "**")

    # Evaluate and return
    return eval(new_expr)

# Queries WolframAlpha to evaluate expr
def _wolfram(expr):

    # Construct API call
    query = expr.replace(" ", "+")
    get = "https://api.wolframalpha.com/v2/query?format=plaintext&output=JSON&appid=" + _app_id + "&input=" + query
    
    # Perform get request
    with req.urlopen(get) as response:

        # Read result into JSON
        result = loads(response.read())['queryresult']
        
        # If successful get result and return
        if result['success']:
            return _strip_unsupported_chars(result['pods'][1]['subpods'][0]['plaintext'])

# Only run if CalCalc.py was called from the command line
if __name__ == "__main__":
    # Loop over each argument
    for i in range(len(sys.argv)):
        arg = sys.argv[i]

        # Check if argument is calculate flag "-s", check that expression is provided as well
        if arg == "-s" and i+1 < len(sys.argv):
            # Extract expression
            expr = sys.argv[i+1]

            # If all characters are supported call calculate
            if _verify_supported_chars(expr):
                # Call calculate and print
                print(_eval_math(expr))
            else:
                print("expression contained unsupported characters")

            # Iterate i to skip expression
            i+=1
        
        # Check if argument is calculate flag "-w", check that expression is provided as well
        elif arg == "-w" and i+1 < len(sys.argv):
            # Extract expression
            expr = sys.argv[i+1]

            # Call wolfram and print
            print(_wolfram(expr))

            # Iterate i to skip expression
            i+=1