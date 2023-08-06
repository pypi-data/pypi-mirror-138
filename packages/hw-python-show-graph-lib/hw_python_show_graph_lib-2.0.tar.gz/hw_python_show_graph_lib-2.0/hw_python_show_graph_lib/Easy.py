def fib(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    else:
        res = [0, 1]
        for i in range(n - 2):
            res.append(res[-1] + res[-2])
        return res
