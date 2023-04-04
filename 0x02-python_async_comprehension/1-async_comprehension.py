#!/usr/bin/env python3

"""
The coroutine will collect 10 random numbers
using an async comprehensing over async_generator
"""

from asyncio import sleep
from random import uniform
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """ async_comprehension that takes no arguments. """
    a = [i async for i in async_generator()]
    return a
