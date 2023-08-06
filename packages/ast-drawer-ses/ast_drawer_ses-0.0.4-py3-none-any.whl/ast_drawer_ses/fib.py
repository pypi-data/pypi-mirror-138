def fib(n):
    assert n >= 0
    # f0,  f1
    f = [0] + [1] * n
    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    return f
