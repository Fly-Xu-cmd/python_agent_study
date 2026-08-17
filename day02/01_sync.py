import time

time_start = time.time()


def task(name):
    print(f"Task {name} started")
    time_start = time.time()
    time.sleep(1)
    time_end = time.time()
    print(f"Task {name} completed in {time_end - time_start:.2f} seconds")


tasks = ["A", "B", "C"]

for task_name in tasks:
    task(task_name)

time_end = time.time()
print(f"All tasks completed in {time_end - time_start:.2f} seconds")
