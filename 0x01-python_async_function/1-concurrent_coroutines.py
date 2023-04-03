#!/usr/bin/env python3
import asyncio
from typing import Callable, List
wait_random: Callable = __import__('0-basic_async_syntax').wait_random

'''
    execute multiple coroutines at the same time with async
'''


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''returns a list of n random floats
    generated using the wait_random coroutine
    '''
    tasks: List[asyncio.Task] = [asyncio.create_task(
        wait_random(max_delay)) for x in range(n)]
    return [await task for task in asyncio.as_completed(tasks)]
