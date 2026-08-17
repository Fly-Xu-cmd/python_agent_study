import time
import asyncio

time_start = time.time()


async def task(name):
    print(f"Task {name} started")
    time_start = time.time()
    # await asyncio.sleep(1)
    time.sleep(1)
    time_end = time.time()
    print(f"Task {name} completed in {time_end - time_start:.2f} seconds")


async def main():
    #     task_A = asyncio.create_task(task("A"))
    #     task_B = asyncio.create_task(task("B"))
    #     task_C = asyncio.create_task(task("C"))

    #     await task_A
    #     await task_B
    #     await task_C
    await asyncio.gather(task("A"), task("B"), task("C"))


asyncio.run(main())

time_end = time.time()
print(f"All tasks completed in {time_end - time_start:.2f} seconds")
