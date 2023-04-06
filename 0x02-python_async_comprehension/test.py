import random
import asyncio
from typing import List

async_generator = __import__('0-async_generator').async_generator

async def async_comprehension() -> List[int]:
    rand = [num async for num in async_generator()]
    return rand
    return await async_generator()

print(asyncio.run(async_comprehension()))