# Python-Stopwatch2

A simple stopwatch for measuring code performance. This is a fork from [python-stopwatch](https://pypi.org/project/python-stopwatch/), which adds static typing and a few other things.

## Status

[![Pypi Downloads](https://pepy.tech/badge/python-stopwatch2)](https://pepy.tech/project/python-stopwatch2)
[![Pypi Version](https://img.shields.io/pypi/v/python-stopwatch2)](https://pepy.tech/project/python-stopwatch2)
[![Tests](https://github.com/devRMA/python-stopwatch2/actions/workflows/tests.yml/badge.svg)](https://github.com/devRMA/python-stopwatch2)
[![Python Versions](https://img.shields.io/pypi/pyversions/python-stopwatch2)](https://www.python.org/)
[![Wheel](https://img.shields.io/pypi/wheel/python-stopwatch2)](https://pypi.org/project/python-stopwatch2/)
[![Coverage Status](https://coveralls.io/repos/github/devRMA/python-stopwatch2/badge.svg)](https://coveralls.io/github/devRMA/python-stopwatch2)
[![Repo Size](https://img.shields.io/github/repo-size/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2)
[![Open Issues](https://img.shields.io/github/issues-raw/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2/issues)
[![License](https://img.shields.io/github/license/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2/blob/main/LICENSE)
[![Stars](https://img.shields.io/github/stars/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2/stargazers)
[![Contributors](https://img.shields.io/github/contributors/devRMA/python-stopwatch2)](https://github.com/devRMA/python-stopwatch2/graphs/contributors)

## Usage

### Installation

To install the library, you can just run the following command:

```shell
poetry add python-stopwatch2
```

Or, using pip:

```shell
pip install python-stopwatch2
```

### Basic usage

#### stopwatch.Stopwatch

You can use the [start()](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstart) and [stop](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstop) methods to starts or stops the stopwatch counter.

```python
from time import sleep

from stopwatch import Stopwatch

my_stopwatch = Stopwatch()
sleep(2)
my_stopwatch.stop()
print(my_stopwatch.elapsed)  # 2.00027129999944
sleep(1)
print(my_stopwatch.elapsed)  # 2.00027129999944
my_stopwatch.start()
sleep(1)
my_stopwatch.stop()
print(my_stopwatch.elapsed)  # 3.0158972999997786
print(f'Time elapsed: {my_stopwatch}')  # Time elapsed: 3.02s
```

It is also possible to use [Stopwatch](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstopwatch) with the [with statement](https://www.geeksforgeeks.org/with-statement-in-python/).

```python
from time import sleep

from stopwatch import Stopwatch

with Stopwatch() as my_stopwatch:
    sleep(3)
print(my_stopwatch.elapsed)  # 3.0012330539993854
print(f'Time elapsed: {my_stopwatch}')  # Time elapsed: 3.00s
```

If you want to print the elapsed time at the end of [with statement](https://www.geeksforgeeks.org/with-statement-in-python/), you can pass the second parameter at stopwatch startup, as True

```python
from time import sleep

from stopwatch import Stopwatch

with Stopwatch('my custom message', True):
    sleep(3)
# [__main__:<module>:5] ~ 3.00s - my custom message
```

#### stopwatch.profile

This decorator is used to profile a function. It will print a report every time the function is called and, at the end of the execution, the final report will be printed.

```python
from time import sleep

from stopwatch import profile


@profile(name='My function')
def wait_for(time: float) -> None:
    sleep(time)


for time in [0.1, 0.2, 0.3, 0.4, 0.5]:
    wait_for(time)
print('end')

# [__main__#My function] hits=1, mean=100.14ms, min=100.14ms, median=100.14ms, max=100.14ms, dev=0.00μs
# [__main__#My function] hits=2, mean=150.20ms, min=100.14ms, median=150.20ms, max=200.26ms, dev=50.06ms
# [__main__#My function] hits=3, mean=200.25ms, min=100.14ms, median=200.26ms, max=300.35ms, dev=81.74ms
# [__main__#My function] hits=4, mean=250.30ms, min=100.14ms, median=250.30ms, max=400.44ms, dev=111.92ms
# [__main__#My function] hits=5, mean=300.35ms, min=100.14ms, median=300.35ms, max=500.55ms, dev=141.56ms
# end
# [__main__#My function] hits=5, mean=300.35ms, min=100.14ms, median=300.35ms, max=500.55ms, dev=141.56ms
```

If the ``name`` parameter is not informed, it will use the function name.

It is also possible to pass the ``report_every`` parameter (which by default is 1) which informs how many times the report should be printed. If ``None`` is passed, the report will only be printed at the end of the execution.

```python
from time import sleep

from stopwatch import profile


@profile(report_every=2)
def report_every2(time: float) -> None:
    sleep(time)


@profile(report_every=None)
def no_report(time: float) -> None:
    sleep(time)


for time in [0.1, 0.2, 0.3, 0.4, 0.5]:
    report_every2(time)
    no_report(time)
print('end')

# [__main__#report_every2] hits=2, mean=150.20ms, min=100.15ms, median=150.20ms, max=200.25ms, dev=50.05ms
# [__main__#report_every2] hits=4, mean=250.30ms, min=100.15ms, median=250.30ms, max=400.46ms, dev=111.92ms
# end
# [__main__#no_report] hits=5, mean=300.36ms, min=100.15ms, median=300.36ms, max=500.58ms, dev=141.57ms
# [__main__#report_every2] hits=5, mean=300.43ms, min=100.15ms, median=300.36ms, max=500.94ms, dev=141.68ms
```

#### stopwatch.stopwatch

This class is to be used with [with statement](https://www.geeksforgeeks.org/with-statement-in-python/) and will print the time it took to execute the code.

```python
from time import sleep

from stopwatch import stopwatch

with stopwatch():
    sleep(0.5)

# [__main__:<module>:5] ~ 500.27ms
```
