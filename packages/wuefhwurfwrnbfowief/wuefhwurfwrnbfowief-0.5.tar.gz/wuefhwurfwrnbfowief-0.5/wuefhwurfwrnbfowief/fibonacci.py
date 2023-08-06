def fibonacci(n):
    fib1 = fib2 = 1
    result = [fib1, fib2]
    n = n - 2
    for i in range(n):
        fib1, fib2 = fib2, fib1 + fib2
        result.append(fib2)
    return result