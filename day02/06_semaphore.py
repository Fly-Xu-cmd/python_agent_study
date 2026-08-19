import asyncio

active_count = 0

semaphore = asyncio.Semaphore(3)  # Limit to 3 concurrent tasks


async def task(name):
    global active_count
    async with semaphore:
        active_count += 1
        print(f"Task {name} started. Active tasks: {active_count}")
        await asyncio.sleep(1)
        active_count -= 1
        print(f"Task {name} completed. Active tasks: {active_count}")


async def main():
    tasks = [task(f"Task-{i}") for i in range(10)]
    await asyncio.gather(*tasks)


asyncio.run(main())
