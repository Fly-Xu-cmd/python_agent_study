import time
import asyncio

time_start = time.time()


async def task(name):
    print(f"Task {name} started")
    time_start = time.time()
    await asyncio.sleep(1)
    time_end = time.time()
    print(f"Task {name} completed in {time_end - time_start:.2f} seconds")


async def main():
    await asyncio.gather(task("A"), task("B"), task("C"))


asyncio.run(main())

time_end = time.time()
print(f"All tasks completed in {time_end - time_start:.2f} seconds")
