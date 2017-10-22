def fib():
    """Infinite Fibonacci generator, starts at 0"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def print_nth_first_fib_numbers(n):
    fib_instance = fib()
    for i in range(n):
        print(next(fib_instance))


if __name__ == "__main__":
    print_nth_first_fib_numbers(20)
