def fib():
    """Infinite Fibonacci generator, starts at 0"""
    a, b = 0, 1
    while True:
        try:
            yield a
        except GeneratorExit:
            print("Let's clean up!")
            raise
        a, b = b, a + b


def print_fib_no_bigger_than(n):
    fib_instance = fib()
    for i in range(n):
        fib_number = next(fib_instance)
        if fib_number > n:
            fib_instance.close()
            break
        print(fib_number)


if __name__ == "__main__":
    print_fib_no_bigger_than(1000)
