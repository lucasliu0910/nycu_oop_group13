class MathUtils:
    @staticmethod
    def add(x, y):
        return x + y
    def multiply(x,y):
        return x * y

def test_add():
    assert add(2,3) == 5
    assert add(-1,1) == 0

def test_multiply():
    assert multiply(2,3) == 6
    assert multiply(0,11) == 0
