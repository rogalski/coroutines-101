![](./pygda.png)
# Coroutines 101
## Lukasz Rogalski

---

### Agenda
1. Problem statement
2. Coroutines
3. Coroutines in Python
4. Code snippets
5. Summary
6. Q&A

---

### Backstory
#### Why this talk?
- I wanted to figure out _new hot thing_ -  `asyncio`
- I eventually learned that it’s just a one of implementations of more basic concept of _coroutines_.
- **Let’s learn how to walk before running**

#### Disclaimer
- I’m not a pro
- Feedback is more than welcome

---

### Problem statement
#### Single threaded code
- single threaded code is easy but often is not enough
- we want to utilize CPU in more efficient manner
- two typical cases which
---
#### Parallelism vs concurrency

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

>Coroutines are computer-program components that generalize subroutines for non-preemptive multitasking, by allowing multiple entry points for suspending and resuming execution at certain locations. Coroutines are well-suited for implementing familiar program components such as cooperative tasks, exceptions, event loops, iterators, infinite lists and pipes.

---
#### Basic properties
- lightweight
- only one coroutine runs at the single point in time (GIL is not an problem!)

#### Where coroutines shine?
IO-bound, network-bound problems!

- We do not use 100% of CPU (we _sleep a lot_ waiting for a response).
- In blocking code we waste a lot of cpu cycles.
- We have spare cpu cycles - why not use them to handle more requests _concurrently_?

Coroutines helps us with exactly that.

---

### Coroutines in Python
#### History
[PEP 255 — Simple Generators](https://www.python.org/dev/peps/pep-0255/) (Python 2.2)

[PEP 342 — Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/) (Python 2.5)
> (…) if it were possible to pass values or exceptions into a generator at the point where it was suspended, a simple co-routine scheduler or trampoline function would let coroutines call each other without blocking -- a tremendous boon for asynchronous applications

[PEP 380 — Syntax for Delegating to a Subgenerator](https://www.python.org/dev/peps/pep-0380/) (Python 3.3)
> (…) if the subgenerator is to interact properly with the caller in the case of calls to `send()`, `throw()` and `close()`, things become considerably more difficult. (…) the necessary code is very complicated, and it is tricky to handle all the corner cases correctly. (…) The following new expression syntax will be allowed in the body of a generator: `yield from <expr>`

---

 [PEP 492 -- Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/) (Py 3.5)
> This proposal makes coroutines a native Python language feature, and clearly separates them from generators. This removes generator/coroutine ambiguity, and makes it possible to reliably define coroutines without reliance on a specific library. This also enables linters and IDEs to improve static code analysis and refactoring.

What we'll focus on:
- [PEP 255 — Simple Generators](https://www.python.org/dev/peps/pep-0255/) (Python 2.2)
- [PEP 342 — Coroutines via Enhanced Generators](https://www.python.org/dev/peps/pep-0342/) (Python 2.5)

---

#### Generators and coroutines
Different in terms of usage
- generators are _producers of data_
- coroutines are _consumers_ of data

Similar in terms of how they work:
- they _receive_ and _give away_ control flow from/to another code
- state is kept when generator/coroutine is re-entered

---

### Code snippets
[TBD]

---

### Summary
#### What we’ve learned
- coroutines as simple way for solving IO-bound problems
- they are run concurrently, only one coroutine runs at single point of time

#### Learn more
##### Computer Science terms
 - coroutines
 - fibers

##### Python implementations:
  - `tornado`
  - `gevent`
  - ` asyncio`, `tulip`, `trollius`
  - `stackless`

Different implementations will expose different APIs, use different names etc.
However, in principle, all of them use same concept of coroutines.

##### Resources
- [David Beazley - A Curious Course on Coroutines and Concurrency (PyCon 2009)](http://www.dabeaz.com/coroutines/Coroutines.pdf)
- [Łukasz Langa - Thinking in coroutines (PyCon 2016)](https://www.youtube.com/watch?v=l4Nn-y9ktd4)

---

# Thank you!
- Slides: https://github.com/rogalski/coroutines-101
- My LinkedIn: https://www.linkedin.com/in/lukasz-rogalski/

---

# Q&A
