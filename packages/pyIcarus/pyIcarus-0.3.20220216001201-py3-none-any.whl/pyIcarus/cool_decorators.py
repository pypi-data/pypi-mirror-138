import time
from atexit import register
from functools import singledispatch

from profilehooks import coverage, timecall


# Use this decorator to have multiple function prototypes (overrides) like in c/c++
@singledispatch
def fun(arg, verbose=False):
    if verbose:
        print("Let me just say,", end=" ")
    print(arg)


@fun.register
def _(arg: int, verbose=False):
    if verbose:
        print("Strength in numbers, eh?", end=" ")
    print(arg)


@fun.register
def _(arg: list, verbose=False):
    if verbose:
        print("Enumerate this:")
    for i, elem in enumerate(arg):
        print(i, elem)


@coverage
def cover_me(val: int):
    if val == 69:
        print('woohoo')
    elif val == 420:
        print("🤢")


@timecall
def time_me(sleep_time):
    time.sleep(sleep_time)


@coverage
@register
def exiting():
    print(" Goodbye!")


if __name__ == '__main__':
    fun(69, True)
    fun([1, 2, 3], True)
    cover_me(69)
    cover_me(420)
    cover_me(1337)
    time_me(0.25)
    time_me(0.5)
