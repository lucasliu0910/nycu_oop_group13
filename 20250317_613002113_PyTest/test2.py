def subtract(a,b):
    return a-b

def divide(a,b):
    if b == 0:
        return None
    return a/b

assert subtract(10,2) == 10-2
assert divide(10,2) == 10/2