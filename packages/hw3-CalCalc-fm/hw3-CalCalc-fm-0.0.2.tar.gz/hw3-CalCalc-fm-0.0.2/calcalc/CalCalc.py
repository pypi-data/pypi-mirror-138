import argparse
import xml.etree.ElementTree as ET 
from urllib.request import urlopen
from urllib.parse import quote_plus

def calculate(s, return_float=False):
    try:
        # refuse access to the builtins
        ans = eval(s, {"__builtins__": {}})
        return(ans)
    # if eval() can't do this, switch to Wolfram instead:
    except:
        appid = "6R6EL8-V4TYXKGK85"
        question = quote_plus(s)
        url = f"http://api.wolframalpha.com/v2/query?input={question}&appid={appid}"
        rawdata = urlopen(url).read()
        # process the xml data
        elements = ET.fromstring(rawdata)
        ans = elements.findall('.//plaintext')[1].text
        ans = ans.split(' ')[0]
        if return_float:
            # correct the answer to match with python syntax, then evaluate
            ans = ans.replace('×', '*')
            ans = ans.replace('^', '**')
            ans = eval(ans)
        return ans

def get_parser():
    parser = argparse.ArgumentParser(description="Evaluate a string")
    parser.add_argument('-s', help="calculate directly from a string")
    parser.add_argument('-w', help="calculate by Wolfram")
    return parser

def test_1():
    assert abs(4. - calculate('2**2')) < 0.001

def test_2():
    assert calculate('34*28') == 952

def test_3():
    assert calculate('mass of the moon in kg', return_float=True)/(10**22) > 7

def test_4():
    assert calculate('mass of the jupyter in kg', return_float=True)/(10**27) < 2

def test_5():
    assert calculate('avogadro number', return_float=True)/(6e23) - 1 < 0.01
    
if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if (args.s != None) and (args.w == None):
        question = args.s
    if (args.s == None) and (args.w != None):
        question = args.w
    if (args.s != None) and (args.w != None):
        print("please input one question only, calculating question 1:")
        question = args.s
    if (args.s == None) and (args.w == None):
        print("please input your question by -s or -w")
    answer = calculate(question)
    print(answer)