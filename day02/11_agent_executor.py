import asyncio
import time

start_time = time.time()
semaphore = asyncio.Semaphore(3)  # 限制同时运行的任务数量为 3
max_retries = 3
timeout = 5  # 设置超时时间为 5 秒


async def search(query):
    await asyncio.sleep(2)
    return f"搜索: {query}"


async def weather(city):
    await asyncio.sleep(2)
    return f"天气: {city}"


async def database(sql):
    await asyncio.sleep(5)
    return f"数据库: {sql}"


async def execute_task(task_func, *args):
    for i in range(max_retries):
        try:
            async with semaphore:
                async with asyncio.timeout(timeout):
                    result = await task_func(*args)
                    print(result)
                    return result
        except Exception as e:
            await asyncio.sleep(2**i)  # 等待一段时间后重试,指数退避 1s, 2s, 4s
            print(f"发生异常: {e}，等待{2**i}秒后重试第 {i + 1} 次...")
            if i == max_retries - 1:
                raise


async def main():
    tasks = [
        execute_task(search, "Python"),
        execute_task(search, "JavaScript"),
        execute_task(search, "Java"),
        execute_task(search, "C++"),
        execute_task(search, "Go"),
        execute_task(search, "Rust"),
        execute_task(search, "Kotlin"),
        execute_task(search, "Swift"),
        execute_task(search, "TypeScript"),
        execute_task(search, "PHP"),
        execute_task(weather, "北京"),
        execute_task(weather, "上海"),
        execute_task(weather, "广州"),
        execute_task(weather, "深圳"),
        execute_task(weather, "杭州"),
        execute_task(database, "SELECT * FROM users"),
        execute_task(database, "SELECT * FROM orders"),
    ]
    result = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"所有任务执行完成:{result}")


asyncio.run(main())

end_time = time.time()
print(f"程序执行时间: {end_time - start_time:.2f} 秒")
