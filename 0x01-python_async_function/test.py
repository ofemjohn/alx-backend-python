from time import time
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random

def task_wait_random(max_delay: int) -> asyncio.tasks:
    task = wait_random(max_delay)
    return asyncio.create_task(task)