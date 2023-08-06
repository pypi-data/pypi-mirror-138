import ast

from hw_1.fib import fib
from hw_1.printer import Traverser

traverser = Traverser()


def process(code: str):
    res = ast.parse(code)
    # a = 1
    traverser.process(res)
    traverser.try_print()


if __name__ == '__main__':
    # print(fib(7))
    program = """def fib(n):
        ans = [1]
        a = b = 1
        for i in range(0, n - 1):
            c = b
            b = a + b
            ans.append(b)
            a = c
            
        return ans
    """

    process(program)
