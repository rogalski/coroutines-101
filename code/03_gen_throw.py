def fib():
    """Infinite Fibonacci generator, starts at 0"""
    a, b = 0, 1
    while True:
        yield a  # thrown exception origins from here (see stacktrace)
        a, b = b, a + b


def print_fib_throw_after(n):
    fib_instance = fib()
    for i in range(n):
        fib_number = next(fib_instance)
        print(fib_number)
        if fib_number == n:
            fib_instance.throw(Exception, Exception("I don't like {0}".format(n)))


if __name__ == "__main__":
    print_fib_throw_after(89)
