import asyncio
import time

time_start = time.time()


async def slow_task():
    await asyncio.sleep(5)


async def main():
    # try:
    #     await asyncio.wait_for(slow_task(), timeout=3)
    # except asyncio.TimeoutError:
    #     print("任务超时！")
    try:
        async with asyncio.timeout(3):
            await slow_task()
    except asyncio.TimeoutError:
        print("任务超时！")


asyncio.run(main())
time_end = time.time()
print(f"程序执行时间: {time_end - time_start:.2f} 秒")
