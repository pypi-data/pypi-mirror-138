def fibonacci(n):
    res = [1, 1]
    for i in range(2, n):
        res.append(res[i - 1] + res[i - 2])
    return res
