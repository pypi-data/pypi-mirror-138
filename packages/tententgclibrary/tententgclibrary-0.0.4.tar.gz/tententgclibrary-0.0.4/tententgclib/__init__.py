def add_numbers(num1 , num2):
    return num1 + num2


def subtract_numbers(num1, num2):
    return num1 - num2

def multiply_numbers(num1, num2):
    return num1 * num2

def divide_numbers(num1, num2):
    return num1 / num2

def mean(a):
    return sum(a) / len(a)

def listfind_odd(a):
    return [x for x in a if x % 2 == 1]

def listfind_even(a):
    return [x for x in a if x % 2 == 0]

def stack(a,b):
    for i in range(1,a+1): 
        print(b*i)
        
def reverse_stack(a,b):
    for i in range(a,0,-1):
        print(b*i)
        
def factorial(a):
    if a == 0:
        return 1
    else:
        return a * factorial(a-1)

def lower_alphabet():
    a = 'abcdefghijklmnopqrstuvwxyz'
    return a

def upper_alphabet():
    a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return a


def is_prime(n):
    if n <= 1:
        return False
    for k in range(2, int(n**0.5)+1):
        if n % k == 0:
            return False
    return True


def next_prime(n):
    n += 1
    while not is_prime(n):
        n += 1
    return n


def next_twin_prime(n):
    n1 = next_prime(n)
    n2 = next_prime(n1)
    while n2 - n1 != 2:
        n1 = n2
        n2 = next_prime(n1)
    return n1, n2
