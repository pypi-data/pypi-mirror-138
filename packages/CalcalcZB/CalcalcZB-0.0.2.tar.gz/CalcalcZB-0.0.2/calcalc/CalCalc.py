"""CalCalc: evaluate strings as numeric expressions. If simple (i.e., no
alpha characters), will try to evaluate locally with numexpr. If more
complex, will try to query wolfram alpha.
"""
import argparse
import numexpr as ne
import urllib.request
import requests


def calculate(str_input, return_float=True):
    """Evaluate any string, limited to numerical expressions.

    Parameters
    ----------
    str_input : str
        String expression to evaluate.
    return_float : bool
        If output should be float (default = True)

    Returns
    -------
    answer : float
        Numeric output of evaluated string.

    """

    # first, are you string?
    if type(str_input) != str:
        raise ValueError("You are not a string. Try again.")

    # let's see if numexpr can solve you
    try:
        answer = ne.evaluate(str_input).item()
        return answer

    except (KeyError, SyntaxError):

        # ok, let's send you to wolfram
        try:
            answer = query_wolfram(str_input, return_float)
            return answer

        except (ValueError, SyntaxError):
            return "idk"


def query_wolfram(str_input, return_float):
    """Send off query to wolfram...

    Parameters
    ----------
    str_input : str
        String expression to evaluate, e.g. 'mass of moon in kg'
    return_float : bool
        If output should be float (default = True)

    Returns
    -------
    query_output : str or float
        Full text restult or just float, depending on 'return_float'

    """

    # note: got some help with json from Brooke and \
    # https://towardsdatascience.com/build-your-next-\
    # project-with-wolfram-alpha-api-and-python-51c2c361d8b9

    # make query url
    app_id = '9TLK2V-8T9H43UY82'
    query = urllib.parse.quote_plus(str_input)

    query_url = f"http://api.wolframalpha.com/v2/query?" \
        f"appid={app_id}" \
        f"&input={query}" \
        f"&format=plaintext" \
        f"&includepodid=Result" \
        f"&output=json"

    # go fetch!
    r = requests.get(query_url).json()

    # wolfram might not be able to execute the computation...
    if r["queryresult"]['numpods'] == 0:
        raise ValueError('Wolfram found nothing to compute.')

    # parse the output
    data = r["queryresult"]["pods"][0]["subpods"][0]
    query_output = data["plaintext"]

    # wolfram might not know the answer....
    if query_output == '(data not available)':
        raise ValueError('Wolfram does not know the answer.')

    # ...but if it does, split out a float...
    # (could probably make this prettier)
    if return_float:
        number = query_output.split(' ')[0]
        number_simple = number.replace('×', '*').replace('^', '**')
        return ne.evaluate(number_simple).item()

    # ... or return the full string result
    else:
        return query_output


if __name__ == '__main__':
    # parse command line arguements
    parser = argparse.ArgumentParser(description='CalCal Module')
    parser.add_argument('-s', action='store', dest='str_input',
                        help='String to parse')
    results = parser.parse_args()

    # TODO: try using click instead to make cuter!

    # check you got an arg
    if results.str_input is None:
        raise ValueError('feed me a string with -s')

    # execute function
    print(calculate(results.str_input))
