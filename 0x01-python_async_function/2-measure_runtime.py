#!/usr/bin/env python3
""" Measure the runtime """

from asyncio import run
from time import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ Measure the runtime """
    start: float = time()

    run(wait_n(n, max_delay))

    end: float = time()

    return (end - start) / n


n = 5
max_delay = 9

print(measure_time(n, max_delay))

