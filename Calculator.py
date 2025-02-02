# -*- coding: utf-8 -*-
"""
@author: Cassie Thun
"""
import tkinter as tk
import math

expression = ""

"""
Transfroms infix expression to post fix 
Then calculates expression
Retruns answer or an error
"""
def calculate(exp):
    post = toPostfix(exp)
    
    #Retruns any errors from toPostFix
    if type(post) != list:
        return post
    
    stack = []
    
    #Loops through post and makes caluclations
    for i in post:
        
        #If token is a number, add to astack
        if isValidNumber(i):
            stack.append(float(i))
        elif isOperator(i):
            #If token is a operator, take last 2 numbers from stack
            #and calculate based on operator
            y = stack.pop()
            x = stack.pop()
            
            #Calculate based on operator
            if i == '+':
                stack.append(x + y)
            elif i == '-':
                stack.append(x - y)
            elif i == '*':
                stack.append(x * y)
            elif i == '/':
                if y == 0:
                    return "Cannot divide by 0"
                stack.append(x / y)
            elif i == '^':
                stack.append(pow(x, y))
            
        elif isFunction(i):
            #If token is a function, calculate with last number on stack
            x = stack.pop()
            
            if 'sin' in i:
                stack.append(math.sin(x))
            elif 'cos' in i:
                stack.append(math.cos(x))
            elif 'tan' in i:
                stack.append(math.tan(x))
            elif 'cot' in i:
                stack.append(1 / math.tan(x))
            elif 'log' in i:
                stack.append(math.log10(x))
            elif 'ln' in i:
                stack.append(math.log(x))
    #Returns answer
    return stack[0]

"""
Using Shunting yard algorithm by Edgar Dijkstra
Takes expression and puts it in postfix
Returns postfix expression or error for incorrect parenthesis
"""
def toPostfix(exp):
    operator = []
    output = []
    tokens = exp.split(" ")
    
    for t in tokens:
        if isValidNumber(t):
            output.append(t)
        elif isFunction(t):
            operator.append(t)
        elif isOperator(t):
            o1 = t
            #checks whether ther is an operator already in the stack
            if len(operator) != 0:
                o2 = operator[len(operator) - 1]
                o1p = precidence(o1)
                o2p = precidence(o2)
                #Orders operators by precidence
                while o2p != 5 and  (o2p > o1p or (o1p == o2p and o1p != "^"))  and len(operator) != 0:
                    output.append(operator.pop())
                    
                    #update o2
                    if len(operator) != 0:
                        o2 = operator[len(operator) - 1]
                    o2p = precidence(o2)
                
            operator.append(o1)
        elif "(" in t or "{" in t:
            operator.append(t)
        elif t == ")" or t == "}":
            #Puts everything between the open parenthesis and closed parenthesis in output
            if len(operator) != 0:
                op = operator[len(operator) - 1]
                while prenPair(t) not in op:
                    if len(operator) == 0:
                        return "Incorrect parenthesis"
                    output.append(operator.pop())
                    if len(operator) != 0:
                        op = operator[len(operator) - 1]
                    
                
                #Remove left parenthesis or adds function to output
                if(isFunction(op)):
                    output.append(operator.pop())
                else:
                    operator.pop()
                #Multiply total by -1 if parenthesis is negative
                if "-" in op:
                    output.append("-1")
                    output.append("*")
                
                
    #puts remaining operators in output stack
    while len(operator) != 0:
        op = operator.pop()
        if op == "(" or op == "{":
            return "Incorrect parenthesis"
        output.append(op)
    
    #checks for opening parenthesis in stack
    if "{" in output or "(" in output:
        return "Incorrect parenthesis"
    
    return output

"""
Takes string and returns if it is a valid number
"""
def isValidNumber(num):
    dec = 0
    mod = 0
    
    #Makes sure string isn't empty
    if len(num) == 0:
        return False
    
    #ignores negative sign
    if num[0] == '-' and len(num) > 1:
        mod = 1
    
    #Loops through each character in string to check for valid numbers and decimals
    for i in range(mod, len(num)):
        if not num[i].isdigit() and not num[i] == '.':
            return False
        elif num[i] == '.':
            #Makes sure there can't be more than 1 dot per number
            if dec == 0:
                dec += 1
            else:
                return False
    return True


"""
Takes a closed parenthesis and returns its open version
"""
def prenPair(pren):
    if pren == ")":
        return "("
    if pren == "}":
        return "{"
    
"""
Takes an operator and returns its precidence value
"""
def precidence(op):
    if op == "^":
        return 4
    elif op == "*" or op == "/":
        return 3
    elif op == "+" or op == "-":
        return 2
    elif op == "(" or op == "{":
        return 5
    else:
        return 0
"""
Takes a string and retruns whether it is a function
"""  
def isFunction(fun):
    if "cos" in fun or "sin" in fun or "tan" in fun or "cot" in fun or "log" in fun or "ln" in fun:
        return True
    return False

"""
Takes a string and returns whether it is an operator
"""
def isOperator(op):
    return op == "*" or op == "/" or op == "+" or op == "-" or op == "^"
       

"""
Based off of Geeks for Geeks simple GUI calculator
link: https://www.geeksforgeeks.org/python-simple-gui-calculator-using-tkinter/

"""
def click(num):
    # point out the global expression variable 
    global expression 
 
    # concatenation of string 
    if num == "." or type(num) == int :
        #CHECK FOR DOUBLE DECIMAL AND IF PRIOR NUMBER IS INT
        if "." in expression and num == ".":
            return
        elif len(expression) == 0:
            expression = str(num)
        elif expression[len(expression) - 1].isdigit() or expression[len(expression) - 1] == ".":
            expression = expression + str(num)
        else:
            expression = expression + " " + str(num)
    
    elif isFunction(num):
        expression = expression + " " + str(num) + "("
    else:
        expression = expression + " " + str(num) 
 
    # update the expression by using set method 
    equation.set(expression) 

# Function to evaluate the final expression 
def equalpress(): 
    # Try and except statement is used 
    # for handling the errors like zero 
    # division error etc. 
 
    # Put that code inside the try block 
    # which may generate the error 
    try: 
 
        global expression 
 
        # eval function evaluate the expression 
        # and str function convert the result 
        # into string 
        total = str(calculate(expression)) 
 
        equation.set(total) 
 
        # initialize the expression variable 
        # by empty string 
        expression = "" 
 
    # if error is generate then handle 
    # by the except block 
    except: 
 
        equation.set(" error ") 
        expression = "" 
 
 
# Function to clear the contents 
# of text entry box 
def clear(): 
    global expression 
    expression = "" 
    equation.set("") 

"""
Makes the previous operand negative
"""
def neg():
    global expression
    
    #Splits expression to check the last token
    tokens = expression.split(" ")
    
    #Makes sure that there is a number or function to add/remove a negative sign from
    if len(tokens) > 0 and not isOperator(tokens[len(tokens) - 1]) and len(expression) > 0:
        
        #Gets last token to make negative
        num = tokens[len(tokens) - 1]
        if len(num) > 0 and num[0] == '-':
            #if there is already a negative sign in frony, remove it
            expression = expression[:-len(num)]
            num = num[1:]
            expression = expression + num
        else:
            #add a negative sign in front of token
            expression = expression[:-len(num)]
            expression = expression + "-" + num
    
    #Update the displayed equation
    equation.set(expression)

"""
Creates the GUI window
"""
if __name__ == "__main__":
    
    #create GUI window
    window = tk.Tk()
    
    #set title
    window.title("Lab 2 Calculator")
    
    # set window size
    #window.geometry("450x150")
    
    # StringVar() is the variable class 
    # we create an instance of this class 
    equation = tk.StringVar() 
    
    #Create textfield for expression
    exp_field = tk.Label(window, textvariable=equation)
    
    exp_field.grid(columnspan=7)
    
    #Create number buttons
    btn0 = tk.Button(text="0",
                     command=lambda: click(0), height=1, width=7)
    btn0.grid(row=5, column=5)
    
    btn1 = tk.Button(text="1",
                     command=lambda: click(1), height=1, width=7)
    btn1.grid(row=4, column=4)
    
    
    btn2 = tk.Button(text="2",
                     command=lambda: click(2), height=1, width=7)
    btn2.grid(row=4, column=5)
    
    btn3 = tk.Button(text="3",
                     command=lambda: click(3), height=1, width=7)
    btn3.grid(row=4, column=6)
    
    btn4 = tk.Button(text="4",
                     command=lambda: click(4), height=1, width=7)
    btn4.grid(row=3, column=4)
    
    btn5 = tk.Button(text="5",
                     command=lambda: click(5), height=1, width=7)
    btn5.grid(row=3, column=5)
    
    btn6 = tk.Button(text="6",
                     command=lambda: click(6), height=1, width=7)
    btn6.grid(row=3, column=6)
    
    btn7 = tk.Button(text="7",
                     command=lambda: click(7), height=1, width=7)
    btn7.grid(row=2, column=4)
    
    btn8 = tk.Button(text="8",
                     command=lambda: click(8), height=1, width=7)
    btn8.grid(row=2, column=5)
    
    btn9 = tk.Button(text="9",
                     command=lambda: click(9), height=1, width=7)
    btn9.grid(row=2, column=6)
    
    #Create operator buttons
    btn_add = tk.Button(text="+",
                     command=lambda: click("+"), height=1, width=7)
    btn_add.grid(row=4, column=7)
    
    btn_sub = tk.Button(text="-",
                     command=lambda: click("-"), height=1, width=7)
    btn_sub.grid(row=3, column=7)
    
    btn_mul = tk.Button(text="*",
                     command=lambda: click("*"), height=1, width=7)
    btn_mul.grid(row=2, column=7)
    
    btn_div = tk.Button(text="/",
                     command=lambda: click("/"), height=1, width=7)
    btn_div.grid(row=1, column=7)
    
    btn_exp = tk.Button(text="^",
                        command=lambda: click("^"), height=1, width=7)
    btn_exp.grid(row=3, column=3)
    
    btn_sin = tk.Button(text="sin",
                     command=lambda: click("sin"), height=1, width=7)
    btn_sin.grid(row=1, column=1)
    
    btn_cos = tk.Button(text="cos",
                     command=lambda: click("cos"), height=1, width=7)
    btn_cos.grid(row=1, column=2)
    
    btn_tan = tk.Button(text="tan",
                     command=lambda: click("tan"), height=1, width=7)
    btn_tan.grid(row=1, column=3)
    
    btn_cot = tk.Button(text="cot",
                     command=lambda: click("cot"), height=1, width=7)
    btn_cot.grid(row=2, column=1)
    
    btn_log = tk.Button(text="log",
                     command=lambda: click("log"), height=1, width=7)
    btn_log.grid(row=2, column=3)
    
    btn_ln = tk.Button(text="ln",
                     command=lambda: click("ln"), height=1, width=7)
    btn_ln.grid(row=2, column=2)
    
    #Create remaining buttons
    btn_clear = tk.Button(text="C",
                     command=lambda: clear(), height=1, width=7)
    btn_clear.grid(row=1, column=4)
    
    btn_opren = tk.Button(text="(",
                          command=lambda: click("("), height=1, width=7)
    btn_opren.grid(row=1, column=5)
    
    btn_clpren = tk.Button(text=")",
                          command=lambda: click(")"), height=1, width=7)
    btn_clpren.grid(row=1, column=6)
    
    btn_obrack = tk.Button(text="{",
                          command=lambda: click("{"), height=1, width=7)
    btn_obrack.grid(row=3, column=1)
    
    btn_clbrack = tk.Button(text="}",
                          command=lambda: click("}"), height=1, width=7)
    btn_clbrack.grid(row=3, column=2)
    
    btn_eq = tk.Button(text="=",
                          command=lambda: equalpress(), height=1, width=7)
    btn_eq.grid(row=5, column=7)
    
    btn_dot = tk.Button(text=".",
                          command=lambda: click("."), height=1, width=7)
    btn_dot.grid(row=5, column=6)
    
    btn_neg = tk.Button(text="+/-",
                          command=lambda: neg(), height=1, width=7)
    btn_neg.grid(row=5, column=4)
    
    window.mainloop()
