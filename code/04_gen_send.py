"""
First, degenerated example of corooutines.

Basically, we:
- create a coroutine instance based on coroutine function
- main delegates work to coroutine
"""
from __future__ import print_function


def my_coroutine(multiplier):
    print("my_coroutine started with multiplier", multiplier)
    received = []
    while True:
        value_to_produce = ''.join(multiplier * char for char in received)
        print('my_coroutine will produce', repr(value_to_produce))
        data_received = yield value_to_produce
        print('my_coroutine received', repr(data_received))
        received.append(data_received)


def main():
    coro = my_coroutine(multiplier=2)
    # "start" coroutine by sending None to it
    # produced value typically does not make sense
    # usually is thrown away
    coro.send(None)

    for char in "ABC":
        print('main sends to coroutine', repr(char))
        received = coro.send(char)
        print('main received from coroutine', repr(received))


if __name__ == "__main__":
    main()
