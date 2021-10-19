import json

import requests
import click
import six
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

from pyfiglet import figlet_format

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def getContentType(answer, conttype):
    return answer.get("content_type").lower() == conttype.lower()


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


def askRequestInformation():
    questions = [
        {
            'type': 'input',
            'name': 'age',
            'message': 'Age: \n(pick a number: [25-50: 0, 50-100: 1, 0-25: 2])\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'input',
            'name': 'workclass',
            'message': 'Work Class: \n(pick a number: [Federal-gov: 0 ,  Local-gov: 1 ,  Never-worked: 2 ,  Private: 3 ,  Self-emp-inc: 4 ,  Self-emp-not-inc: 5 ,  State-gov: 6 ,  Without-pay: 7])\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'input',
            'name': 'education',
            'message': 'Education: \n(pick a number: [10th: 0 ,  11th: 1 ,  12th: 2 ,  1st-4th: 3 ,  5th-6th: 4 ,  7th-8th: 5 ,  9th: 6 ,  Assoc-acdm: 7 ,  Assoc-voc: 8 ,  Bachelors: 9 ,  Doctorate: 10 ,  HS-grad: 11 ,  Masters: 12 ,  Preschool: 13 ,  Prof-school: 14 ,  Some-college: 15])\n',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'education-num',
            'message': 'Years of Education: (input how many year you studied)',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'marital-status',
            'message': 'Marital status:  \n(pick a number: [Divorced: 0 ,  Married-AF-spouse: 1 ,  Married-civ-spouse: 2 ,  Married-spouse-absent: 3 ,  Never-married: 4 ,  Separated: 5 ,  Widowed: 6])\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'input',
            'name': 'occupation',
            'message': 'Occupation: \n(pick a number: [Adm-clerical: 0 ,  Armed-Forces: 1 ,  Craft-repair: 2 ,  Exec-managerial: 3 ,  Farming-fishing: 4 ,  Handlers-cleaners: 5 ,  Machine-op-inspct: 6 ,  Other-service: 7 ,  Priv-house-serv: 8 ,  Prof-specialty: 9 ,  Protective-serv: 10 ,  Sales: 11 ,  Tech-support: 12 ,  Transport-moving: 13])\n',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'relationship',
            'message': 'Status of relationship: \n(pick a number: [Husband: 0 ,  Not-in-family: 1 ,  Other-relative: 2 ,  Own-child: 3 ,  Unmarried: 4 ,  Wife: 5])\n',
            'validate': EmptyValidator

        },
        {
            'type': 'input',
            'name': 'hours-per-week',
            'message': 'how many working hours per week: \n(pick a number: >60: 0 , <20: 1 , between 20-40:2 ])\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'input',
            'name': 'native-country',
            'message': 'Native country: \n(pick a number: [United-States: 0 , Other: 1])\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'input',
            'name': 'capital-diff',
            'message': 'capital difference: input => capital gain - capital loss\n',
            'validate': EmptyValidator,
        },
        {
            'type': 'confirm',
            'name': 'send',
            'message': 'Do you want to send now'
        }
    ]

    answers = prompt(questions, style=style)
    print(answers)
    return answers


def _decode(o):
    # Note the "unicode" part is only for python2
    if isinstance(o, str):
        try:
            return int(o)
        except ValueError:
            return o
    elif isinstance(o, dict):
        return {k: _decode(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_decode(v) for v in o]
    else:
        return o


@click.command()
def main():
    """
    Simple CLI for sending API calls
    """
    log("Census API", color="blue", figlet=True)
    log("Predict income via our API. Please fill in the parameters of your request.", "green")
    test = True
    while test :
        mailinfo = askRequestInformation()
        if mailinfo.get("send", False):
            try:
                """ Make API CALL """
                url = 'https://census-model-api.herokuapp.com/post/'

                mailinfo.pop('send', None)
                log(json.loads(json.dumps(mailinfo), object_hook=_decode), "blue")
                r = requests.post(url, json=json.loads(json.dumps(mailinfo), object_hook=_decode))
                print(r, r.text)
                log(r.text["results"]["results"], "blue")
            except Exception as e:
                raise Exception("An error occured: %s" % (e))


if __name__ == '__main__':
    main()
