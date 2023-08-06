import requests
import json


def calculate(expression):
    """A function that takes in any string input and calculates the answer. It can do any basic python
       math expressions and even advanced questions like... 'what's the meaning of life?' 

    Args:
        expression ([str]): must be a string asking the question, it can do python syntax or standard Wolfram syntax.

    Raises:
        AssertionError: Don't try to feed it anything like system/os commands, that can lead to a lot of trouble.
        TypeError: We assume the expression you give is a string, if not calculate will error.

    Returns:
        [any]: The code can output any type it deems fit, if python would normally give your expression as an int, it 
        will be an int, a float will be a float etc... more sophisticated questions will be given in string format.
    """

    if "os.system" in expression or "rm " in expression or "-rf" in expression:
        raise AssertionError(
            "Sorry, no funny business here, ask reasonable things please."
        )

    elif isinstance(expression, str) == False:
        raise TypeError("You need to feed me a string!")

    else:
        try:
            answer = eval(expression)
        except:
            response = requests.get(
                "http://api.wolframalpha.com/v2/query?appid=8QX38H-JPXAX5PRGE&input={}&output=JSON".format(
                    expression
                )
            )
            response_dict = json.loads(response.text)

            for i in range(len(response_dict["queryresult"]["pods"])):
                if response_dict["queryresult"]["pods"][i]["title"] == "Result":
                    answer = response_dict["queryresult"]["pods"][i]["subpods"][0][
                        "plaintext"
                    ]
                    return answer

            answer = "I don't know the answer to that unfortunately, ask something else or be more specific and quantifiable."
        finally:
            return answer


###########################################
#                  Tests                  #
###########################################


def test_prevent_os_operations_1():
    try:
        calculate("os.system")
    except:
        assert True
    else:
        assert False


def test_prevent_os_operations_2():
    try:
        calculate("rm ")
    except:
        assert True
    else:
        assert False


def test_prevent_os_operations_3():
    try:
        calculate("-rf")
    except:
        assert True
    else:
        assert False


def test_basic_operations():
    assert 30 - calculate("7 * 4") == 2


def test_wolfram_basic_operations():
    assert (
        calculate("what is the mass of the moon in kg") == "7.3459×10^22 kg (kilograms)"
    )


def test_fail_wolfram_operation():
    assert (
        calculate("what is the average lifespan")
        == "I don't know the answer to that unfortunately, ask something else or be more specific and quantifiable."
    )


def test_invalid_arg_int():
    try:
        not_string_variable = 1
        calculate(not_string_variable)
    except:
        assert True
    else:
        assert False


def test_invalid_arg_list():
    try:
        not_string_variable = [1, 2]
        calculate(not_string_variable)
    except:
        assert True
    else:
        assert False
