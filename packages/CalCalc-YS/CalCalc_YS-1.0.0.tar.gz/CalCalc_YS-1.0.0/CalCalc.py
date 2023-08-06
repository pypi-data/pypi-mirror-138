
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import re

def calculate_wolfram(expression_string, return_float = False):
    expression_string = expression_string.replace('+',r'%2B')
    expression_string = expression_string.replace(' ','+')
    xml_data = urllib.request.urlopen(r"http://api.wolframalpha.com/v2/query?input=" + expression_string + r"&appid=J4P2H2-9W7664X58Y").read()
    root = ET.fromstring(xml_data)
    numeric_const_pattern = r"""
         [-+]? # optional sign
         (?:
             (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
             |
             (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
         )
         # followed by optional exponent part if desired
         (?: [Ee] [+-]? \d+ ) ?
         """  
    # This pattern is borrowed from https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
    
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    count = 0
    pt_pre = 'Invalid Input'
    for pt in root.findall('.//plaintext'):
        if (pt.text):
            if (count == 1):
                result_text = pt.text
                if (return_float == False):
                    return result_text
                else:
                    result_list = rx.findall(result_text.replace("×10^", "e"))
                    return float(result_list[0])
                    #if len(result_list) == 1:
                    #    return float(result_list[0])
                    #else:
                    #    return [float(result_list[i]) for i in range(len(result_list))]
                count = -1
                break
            pt_pre = pt.text  #In case the output only has one line
            count += 1
    if count != -1:
        return pt_pre
    
def calculate(expression_string, return_float = False):
    if (expression_string.find('__') == -1) and (expression_string.find('^') == -1):
        try:
            return eval(expression_string, {'__builtins__':{}})
        except:
            return calculate_wolfram(expression_string, return_float)
    elif (expression_string.find('^') != -1):
        return calculate_wolfram(expression_string, return_float)
    else:
        return r"Invalid Input Including '__'"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculator')
    parser.add_argument('-s', action='store', dest='expression_string',
                        help='Calculate an expression from input')
    parser.add_argument('-w', action='store', dest='expression_string_w',
                        help='Calculate an expression from input via Wolfram Alpha')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    results = parser.parse_args()
    if (results.expression_string != None):
        print(calculate(results.expression_string))
    if (results.expression_string_w != None):
        print(calculate_wolfram(results.expression_string_w))
