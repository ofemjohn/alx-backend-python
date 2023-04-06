#!/usr/bin/env python3

"""Run a comprehension asynchronously"""

from asyncio import gather
from time import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ measure_runtime should measure the total runtime and return it. """
    start = time()
    tasks = [async_comprehension() for i in range(4)]
    await gather(*tasks)
    end = time()
    print(tasks)
    return (end - start)
