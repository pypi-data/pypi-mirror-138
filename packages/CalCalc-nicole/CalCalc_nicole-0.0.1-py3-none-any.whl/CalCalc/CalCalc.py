import numexpr as ne
import argparse
import urllib.request

def calculate(inputstr, return_float=False):
    if return_float: 
        formattedstr=inputstr.replace("+", " plus ")
        formattedstr=formattedstr.replace(" ", "+")
        try: x=urllib.request.urlopen('http://api.wolframalpha.com/v1/result?appid=2XXR7Y-GYX68KT2Y5&i='+formattedstr)
        except: ans='Error: Wolfram coulnd\'t parse'
        else: 
            ans_str=x.read().decode('utf-8')
            
            #handle sci notation
            ans_str=ans_str.replace(" times 10 to the ", "e+")
            
            #select out float w/o assuming format
            ans,prev_ans=0.0,0.0
            for i in ans_str.split():
                try: 
                    prev_ans=ans
                    ans=float(i) 
                except: 
                    ans=prev_ans
    else:
        try: ans=ne.evaluate(inputstr)
        except: ans='Error: Not an algebraic expression, call -w in command line or set return_float=True to ask wolfram'
        
        #cast as float if any input values were float, otherwise cast as int
        if '.' in inputstr:
            ans=float(ans)
        else:
            ans=int(ans)
            
    return ans




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate')
    parser.add_argument('-s', action='store', dest='localstr',default=False,help='compute locally') 
    parser.add_argument('-w', action='store', dest='wolframstr',default=False,help='outsource to wolfram')  
    results = parser.parse_args()
    if results.localstr:
        print(calculate(results.localstr))
    elif results.wolframstr:
        print(calculate(results.wolframstr, return_float=True))
              
        
def test_addition_local():
    assert calculate('35+28') == 63
    assert calculate('35+-20') == 15

def test_multiplication_local():
    assert calculate('35*28') == 980
    assert calculate('25*-4') == -100
    
def test_type_local():
    assert type(calculate('35*28')) == type(980)
    assert type(calculate('35*28.')) == type(980.)
    
def test_addition_wolfram():
    assert calculate('35+28',return_float=True)== 63.0
    
def test_type_wolfram():
    assert type(calculate('35+28',return_float=True)) == type(63.)
    
def test_multiplication_wolfram():
    assert calculate('35*28',return_float=True)*10 == 9800.0
    
def test_distace_wolfram():
    assert calculate('mass of the moon in kgs',return_float=True)==7.3459e+22
    
def test_mass_wolfram():
    assert calculate('distance from la to ny',return_float=True)== 2378.0
    
