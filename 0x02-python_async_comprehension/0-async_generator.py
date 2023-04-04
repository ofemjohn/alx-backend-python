#!/usr/bin/env python3
""" Async Comprehensions """

from asyncio import sleep
import asyncio
from random import uniform
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Generate random numbers between 0 and 10"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
