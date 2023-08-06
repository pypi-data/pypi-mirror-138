def fib(n: int) -> int:
    assert n > 0
    if n == 1 or n == 2:
        return 1
    temp1, temp2 = 1, 1
    for _ in range(n - 2):
        temp1, temp2 = temp2, temp1 + temp2
    return temp2
