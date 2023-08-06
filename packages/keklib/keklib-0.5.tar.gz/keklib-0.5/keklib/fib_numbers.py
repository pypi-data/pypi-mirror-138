def fib_numbers(n):
    res = [1, 1]
    fib_num1 = fib_num2 = 1
    for i in range(2, n):
        fib_num3 = fib_num1 + fib_num2
        fib_num1 = fib_num2
        fib_num2 = fib_num3
        res.append(fib_num2)
    return res
