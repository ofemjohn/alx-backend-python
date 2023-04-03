#!/usr/bin/env python3
import asyncio
import random

'''
    asynchronous coroutine that takes in an integer argument
'''


async def wait_random(max_delay=10):
    '''awaites a random number from 0 -10'''
    wait = random.uniform(0, max_delay)
    await asyncio.sleep(wait)
    return wait
