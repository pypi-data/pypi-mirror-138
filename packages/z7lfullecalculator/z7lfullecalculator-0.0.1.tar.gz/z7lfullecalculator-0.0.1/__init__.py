def add_number(num1, num2):
    return num1 + num2

def subtract_number(num1, num2):
    return num1 - num2

def multiply_number(num1, num2):
    return num1 * num2

def divide_number(num1, num2):
    return num1 / num2

def full_Calculator():
    print("Type First Number")

    num1 = float(input())

    print("Type Second Number")

    num2 = float(input())

    print("Type + to Add Numbers - Type - to Subtract Numbers - Type * to Multiply Number - Type / to Divide Numbers")

    type1 = input()

    if type1 == "+":
        return (num1 + num2)

    if type1 == "-":
        return (num1 - num2)

    if type1 == "*":
        return (num1 * num2)

    if type1 == "/":
        return (num1 / num2)