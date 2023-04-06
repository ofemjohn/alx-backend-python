import asyncio
from typing import List
wait_random = __import__('test').wait_random

async def wait_n(n: int, max_delay: int) -> List[float]:
  tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
  return [await task for task in asyncio.as_completed(tasks)]


print(asyncio.run(wait_n(5, 5)))
print(asyncio.run(wait_n(10, 7)))
print(asyncio.run(wait_n(10, 0)))