import asyncio
import time
import random

start_time = time.time()
max_retries = 3


async def random_task(name):
    await asyncio.sleep(2)
    if name == "B":
        raise ValueError("任务执行失败")
    print(f"任务 {name} 成功完成！")


async def main():
    for i in range(max_retries):
        try:
            return await asyncio.gather(random_task(chr(65 + random.randint(0, 1))))
        except Exception as e:
            await asyncio.sleep(2**i)  # 等待一段时间后重试,指数退避 1s, 2s, 4s
            print(f"发生异常: {e}，等待{2**i}秒后重试第 {i + 1} 次...")
            if i == max_retries - 1:
                raise


try:
    asyncio.run(main())
except Exception as e:
    print(f"最终失败: {e}")
end_time = time.time()
print(f"程序执行时间: {end_time - start_time:.2f} 秒")
