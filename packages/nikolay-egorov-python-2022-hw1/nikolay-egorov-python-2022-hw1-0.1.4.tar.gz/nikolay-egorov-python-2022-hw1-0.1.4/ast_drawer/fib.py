def fib(n):
    ans = [1]
    a = b = 1
    for i in range(0, n - 1):
        c = b
        b = a + b
        ans.append(b)
        a = c

    return ans
