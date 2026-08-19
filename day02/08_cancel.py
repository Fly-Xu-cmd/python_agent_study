import asyncio
import time

start_time = time.time()


async def slow_task():
    await asyncio.sleep(10)


async def main():
    task = asyncio.create_task(slow_task())
    await asyncio.sleep(2)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("任务被取消！")


asyncio.run(main())
end_time = time.time()
print(f"程序执行时间: {end_time - start_time:.2f} 秒")
