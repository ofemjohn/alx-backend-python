import asyncio
from typing import List
from concurrent.futures import FIRST_COMPLETED
from typing import Callable
wait_random: Callable = __import__('0-basic_async_syntax').wait_random
'''
returns a list of n random flo
ats generated using the wait_random coroutine
'''


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''
    Spawns wait_random n times with the specified
    max_delay and returns the delays in ascending order
    '''
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    delays = []
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
        for task in done:
            delays.append(await task)
    return delays
