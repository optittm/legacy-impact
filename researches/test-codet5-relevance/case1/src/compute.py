def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def mult(a, b):
    return a * b

def divide(a, b):
    return a / b

def division(a , b):
    if b == 0:
        raise MemoryError("Not the right exception")
    return a  / b


if __name__ == "__main__":
    divide(1,0)