import asyncio
import time

start_time = time.time()


async def successful_task(name):
    await asyncio.sleep(2)
    print(f"任务 {name} 成功完成！")


async def failing_task(name):
    await asyncio.sleep(2)
    raise ValueError("任务执行失败")


async def main():
    tasks = [
        asyncio.create_task(successful_task("A")),
        asyncio.create_task(failing_task("B")),
        asyncio.create_task(successful_task("C")),
    ]

    try:
        # await asyncio.gather(*tasks)
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        print(f"发生异常: {e}")


asyncio.run(main())
end_time = time.time()
print(f"程序执行时间: {end_time - start_time:.2f} 秒")
