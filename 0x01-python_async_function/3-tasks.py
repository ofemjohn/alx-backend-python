#!/usr/bin/env python3
""" async function """
from typing import Callable
import asyncio

wait_random: Callable = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """ Return an asyncio.Task """
    task: asyncio.Task = asyncio.create_task(wait_random(max_delay))
    return task
