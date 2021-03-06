![](assets/pygda.png)
# Coroutines 101
## Łukasz Rogalski

---

### Agenda
1. Problem statement
2. Coroutines
3. Coroutines in Python
4. Event loops
5. Summary
6. Q&A

---

### Backstory
#### Why I prepared this talk?
- I wanted to figure out _new hot thing_ -  `asyncio`
- Preparing a talk seemed a good way to keep myself motivated and making sure I understand topic well enough to explain it
- I eventually learned that it’s just a one of implementations of more basic concept of _coroutines_.
- **Let’s learn how to walk before running**

#### What can you expect from this talk?
- ~~Being prepared to write production-ready code right away~~
- Understanding basic concepts
- Knowing what to google if you want to start using it

---

#### Disclaimer
- I’m not a pro
- Feedback is more than welcome

---

### Problem statement
- single threaded code - easy to implement and to reason about, but often is not enough
- two typical cases which may be encountered:
  - CPU core usage at 100%, more processing power needed
  - CPU cycles wasted on waiting for something (e.g. response from HTTP request)

**We want to utilize CPU in more efficient manner**

---
#### [Parallelism vs concurrency](https://stackoverflow.com/questions/1050222/concurrency-vs-parallelism-what-is-the-difference)

> Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once.

//TBD: best visualisation
##### Parallelism
```
    /------------\
---/ ------------ \--->
                     t
```

##### Concurrency
```
    /--   -    --\
---/   --- ----   \--->
                     t
```

---

### Coroutines
#### Definition
From Wiki:

>Coroutines are computer-program components that generalize subroutines for **non-preemptive** **multitasking**, by allowing **multiple entry points for suspending and resuming execution** at certain locations. Coroutines are **well-suited** for implementing familiar program components such as cooperative tasks, exceptions, event loops, iterators, infinite lists and pipes.

---
#### Basic properties
- lightweight
- only one coroutine runs at the single point in time (GIL is not an problem)

---

#### Where coroutines shine?
IO-bound, network-bound problems.

- We do not use 100% of CPU (we _sleep a lot_ waiting for a response)
- In blocking code we waste a lot of cpu cycles
- We have spare cpu cycles - why not use them to handle more requests _concurrently_?

Coroutines helps us with that.

---

### Coroutines in Python
#### History
[PEP 255 — Simple Generators](https://www.python.org/dev/peps/pep-0255/) (2001, Python 2.2)

[PEP 342 — Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/) (2005, Python 2.5)
> (…) if it were possible to pass values or exceptions into a generator at the point where it was suspended, a simple co-routine scheduler or trampoline function would let coroutines call each other without blocking -- a tremendous boon for asynchronous applications

---

[PEP 380 — Syntax for Delegating to a Subgenerator](https://www.python.org/dev/peps/pep-0380/) (2009, Python 3.3)
> (…) if the subgenerator is to interact properly with the caller in the case of calls to `send()`, `throw()` and `close()`, things become considerably more difficult. (…) the necessary code is very complicated, and it is tricky to handle all the corner cases correctly. (…) The following new expression syntax will be allowed in the body of a generator: `yield from <expr>`

---

 [PEP 492 -- Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/) (2015, Python 3.5)
> This proposal makes **coroutines a native Python language feature**, and clearly separates them from generators. This removes generator/coroutine ambiguity, and makes it possible to reliably define coroutines without reliance on a specific library. This also enables linters and IDEs to improve static code analysis and refactoring.

---

What we'll focus on:
- [PEP 255 — Simple Generators](https://www.python.org/dev/peps/pep-0255/) (Python 2.2)
- [PEP 342 — Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/) (Python 2.5)

---

### Generators and coroutines
#### Generators
- Intuitive interpretation of generator - to produce value on demand
- `generator.next()` (Python 2.x) / `generator.__next__()` (Python 3.x)
- "Hello world!" for generators - Fibonacci sequence

```python
def fib():
    """Infinite Fibonacci generator, starts at 0"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

---

#### "Those weird generator methods"

##### [`generator.close()`](https://docs.python.org/3/reference/expressions.html#generator.close)
- used to clean-up any resources used within generator
- called by garbage collector
- may be caught in coroutine, but only valid action is to re-raise, otherwise  `RuntimeError: generator ignored GeneratorExit` is raised
- [sometimes it's not that obvious](https://stackoverflow.com/questions/44005817)

---

##### [`generator.throw(type, value=None, traceback=None)`](https://docs.python.org/3/reference/expressions.html#generator.send)
`throw` raises exception as it if would be raised _from within generator_

```python
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
```

---

Stacktrace:

```
Traceback (most recent call last):
  File "/Users/rogalski/Repo/coroutines-101/code/03_gen_throw.py", line 19, in <module>
    print_fib_throw_after(89)
  File "/Users/rogalski/Repo/coroutines-101/code/03_gen_throw.py", line 15, in print_fib_throw_after
    fib_instance.throw(Exception, Exception("I don't like {0}".format(n)))
  File "/Users/rogalski/Repo/coroutines-101/code/03_gen_throw.py", line 5, in fib
    yield a  # thrown exception origins from here (see stacktrace)
Exception: I don't like 89
```

- Note that we established a form of communication channel between caller and coroutine
- We may catch this exception form within a coroutine and act on it accordingly
- **We can affect running coroutine from outside world**

---

##### [`generator.send(val)`](https://docs.python.org/3/reference/expressions.html#generator.send)
- most frequently misunderstood feature of generators
- a lot of misleading examples over the Web
- ~~changing yield values of running generators~~ (?)
- **consuming** values (!)

---

#### Generators vs. coroutines
##### Similar in terms of how they work:
- they _receive_ and _give away_ control flow from/to another code
- state is kept when generator/coroutine is re-entered

##### Different in terms of usage:
- generators are _producers_ of data
- coroutines are _consumers_ of data

##### Relation between generators and coroutines
- generator is a coroutine where consumed value is thrown away
- response in generator depends only on internal state of coroutine

---

### First coroutine
```python
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
    coro.send(None)  # "start" coroutine by sending None to it

    for char in "ABC":
        print('main sends to coroutine', repr(char))
        received = coro.send(char)
        print('main received from coroutine', repr(received))


if __name__ == "__main__":
    main()
```

---

### What we can see?
- running coroutine keeps it's state when re-entered
- context-switching occurs in precisely defined places (`yield` statements)
- produced values depends both on coroutine state (arguments, local namespace) and sent value

---

### Event loop
Interpretation: "main", schedules and triggers execution of coroutines.

Different terminologies:
- event loop
- trampoline function
- scheduler
- ...

---

- no "built-in" implementation (unless you treat `asyncio` as one)
- still, there is core functionality which event loop should provide

---

### Access to kernel-provided event mechanism

##### asyncio
> class `asyncio.SelectorEventLoop`
> Event loop based on the selectors module. Subclass of `AbstractEventLoop`.
>
> Use the most efficient selector available on the platform.
>
> On Windows, only sockets are supported (ex: pipes are not supported): see the MSDN documentation of select.

[Classes hierarchy](https://docs.python.org/3/library/selectors.html#module-selectors):
```
BaseSelector
+-- SelectSelector
+-- PollSelector
+-- EpollSelector
+-- DevpollSelector
+-- KqueueSelector
```

--- 

##### [tornado](http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop)
```python
class IOLoop(Configurable):
    """A level-triggered I/O loop.

    We use ``epoll`` (Linux) or ``kqueue`` (BSD and Mac OS X) if they
    are available, or else we fall back on select(). If you are
    implementing a system that needs to handle thousands of
    simultaneous connections, you should use a system that supports
    either ``epoll`` or ``kqueue``.
```

---

### Access to kernel-provided event mechanism
- `epool` (linux kernel) / `kqueue` (BSD kernel) - `select`-like, but better in terms of efficiency
- allows to avoid using busy loops
- essential for networking high performance

---

### Time awareness
##### [asyncio: delayed calls](https://docs.python.org/3/library/asyncio-eventloop.html#delayed-calls)

> The event loop has its own internal clock for computing timeouts. Which clock is used depends on the (platform-specific) event loop implementation; **ideally it is a monotonic clock**. This will generally be a different clock than `time.time()`.

> `AbstractEventLoop.call_later(delay, callback, *args)`
> 
> Arrange for the callback to be called after the given delay seconds (either an int or float).

> `AbstractEventLoop.call_at(when, callback, *args)`
> Arrange for the callback to be called at the given absolute timestamp when (an int or float), using the same time reference as AbstractEventLoop.time().

> `AbstractEventLoop.time()`
> Return the current time, as a float value, according to the event loop’s internal clock.

---
##### tornado
> `IOLoop.add_timeout(deadline, callback, *args, **kwargs)`
> Runs the callback at the time deadline from the I/O loop.

> `IOLoop.call_later(delay, callback, *args, **kwargs)`
>
> Runs the callback after delay seconds have passed.


---
### Time awareness
- common pattern across event loops
- useful for implementing timeouts

---

### Event loop, many coroutines (asyncio)

[![](assets/tulip_coro.png)](https://docs.python.org/3/library/asyncio-task.html#example-chain-coroutines)

---

## Summary
#### What we’ve learned
- coroutines as simple way for solving IO-bound / network-bound problems
- they are run concurrently, only one coroutine is active at single point of time
- places where context-switching occurs are well defined
- scheduler code is responsible for triggering all coroutines
- coroutines runs part of their functionality, reschedules themselves in event loop and yields control

---

## Learn more
#### Computer Science terms
 - coroutines
 - fibers

#### Python implementations:
  - `tornado`
  - `gevent`
  - ` asyncio`, `tulip`, `trollius`
  - `stackless`

Different implementations will expose different APIs, use different names etc.
However, in principle, all of them use same concepts.

---

## Resources
- [David Beazley - A Curious Course on Coroutines and Concurrency (PyCon 2009)](http://www.dabeaz.com/coroutines/Coroutines.pdf)
- [Łukasz Langa - Thinking in coroutines (PyCon 2016)](https://www.youtube.com/watch?v=l4Nn-y9ktd4)

---

## Thank you!
- Slides: https://github.com/rogalski/coroutines-101
- My LinkedIn: https://www.linkedin.com/in/lukasz-rogalski/

---

# Q&A
