# Day 02：Python asyncio —— 异步执行模型与并发控制

## 1. 学习目标

本阶段目标：

```text
Python 异步执行模型
        ↓
Coroutine
        ↓
Task
        ↓
Event Loop
        ↓
await
        ↓
并发执行
        ↓
Semaphore
        ↓
Timeout
        ↓
Cancellation
        ↓
Exception Handling
        ↓
Retry / Backoff
        ↓
Agent Tool Executor
```

最终能够理解：

> `asyncio` 不负责让 CPU 计算本身变快，而是通过 Event Loop 在 I/O 等待期间调度其他任务，提高 I/O 密集型系统的吞吐能力。

---

# 2. 核心概念

## 2.1 同步执行

普通同步函数：

```python
def task():
    ...
```

调用后会直接执行。

例如：

```text
A → 等待 1 秒 → 完成
B → 等待 1 秒 → 完成
C → 等待 1 秒 → 完成
```

总时间约：

```text
3 秒
```

---

## 2.2 `async def`

```python
async def task():
    ...
```

调用：

```python
coro = task()
```

得到的是：

> Coroutine Object

而不是最终结果。

理解为：

```text
普通函数：
调用 → 执行 → 返回结果

异步函数：
调用 → 得到 Coroutine → 等待执行
```

---

# 3. Coroutine

Coroutine 可以理解为：

> 一个可以被事件循环调度的异步计算对象。

基本关系：

```text
Coroutine
    ↓
create_task()
    ↓
Task
```

---

# 4. Task

```python
task = asyncio.create_task(coro)
```

`create_task()` 的作用不是创建 Event Loop，而是：

> **将 Coroutine 包装成 Task，并安排到当前运行的 Event Loop 中调度。**

整体关系：

```text
asyncio.run()
    ↓
运行 Event Loop
    ↓
create_task()
    ↓
Coroutine → Task
    ↓
Event Loop 调度
```

---

# 5. Event Loop

Event Loop 可以理解为：

> **负责调度异步任务的核心运行机制。**

例如：

```text
              Event Loop
             /    |    \
            ↓     ↓     ↓
         Task A Task B Task C
            │     │     │
          await  await  await
            │     │     │
          I/O等待 I/O等待 I/O等待
```

当一个 Task 因为 I/O 暂时无法继续时，Event Loop 可以调度其他可运行 Task。

---

# 6. `await`

`await` 的核心作用：

> 当前协程需要等待一个尚未完成的 Awaitable 时，暂停当前协程，并把控制权交给事件循环。

例如：

```python
async def task():
    await asyncio.sleep(1)
```

执行模型：

```text
Task A
 ↓
await I/O
 ↓
暂时不能继续
 ↓
Event Loop
 ↓
运行 Task B
```

注意：

> `await` 不等于“自动并发”。

---

# 7. `await` 为什么仍然可能是串行？

例如：

```python
await task_a()
await task_b()
```

执行逻辑：

```text
A → 完成 → B → 完成
```

因此：

```text
async ≠ 并发
await ≠ 并发
```

真正需要让多个任务重叠运行，需要把它们交给 Event Loop 调度。

---

# 8. `asyncio.gather()`

例如：

```python
await asyncio.gather(
    task_a(),
    task_b(),
    task_c(),
)
```

可以让多个 Awaitable 被并发推进。

注意：

> 这里应该使用“并发”，而不是“并行”。

### 并发

多个任务在时间上交错推进：

```text
A → 等待
B → 运行
C → 等待
A → 继续
```

### 并行

多个任务同时运行在不同 CPU 核心。

`asyncio` 的主要能力属于：

> **单线程事件循环上的并发。**

---

# 9. `create_task()` 与 `gather()` 实验

实际实验中：

```python
task_A = asyncio.create_task(task("A"))
task_B = asyncio.create_task(task("B"))
task_C = asyncio.create_task(task("C"))

await task_A
await task_B
await task_C
```

验证了：

> 虽然最终依次 `await`，但 Task 在创建时已经被安排给 Event Loop，因此多个 Task 可以重叠执行。

另外也完成：

```python
await asyncio.gather(
    task("A"),
    task("B"),
    task("C"),
)
```

验证了多个异步任务可以并发执行。

---

# 10. 异步函数中的阻塞代码

一个非常重要的坑：

```python
async def task():
    time.sleep(1)
```

虽然函数声明为 `async def`，但：

```python
time.sleep()
```

仍然是同步阻塞调用。

结果：

```text
Event Loop
 ↓
time.sleep()
 ↓
当前线程被阻塞
 ↓
其他 Task 无法正常调度
```

因此：

> **`async def` 不会自动把内部所有代码变成异步。**

---

# 11. `asyncio` 最适合解决什么问题？

适合：

```text
HTTP 请求
LLM API
MySQL / 数据库
Redis
WebSocket
SSE
其他网络 I/O
```

不适合单纯依靠 `asyncio` 解决：

```text
CPU 密集计算
大规模图像处理
复杂数学计算
模型训练
```

核心判断：

> **这个任务是在等待外部资源，还是主要消耗 CPU？**

---

# 12. Agent 为什么特别适合异步？

Agent 中经常出现：

```text
             Agent
           /   |   \
          ↓    ↓    ↓
       LLM API Search DB
```

这些操作大量时间用于：

```text
等待网络
等待数据库
等待外部服务
```

异步可以让：

```text
Task A 等待 LLM
       ↓
Event Loop 处理 Task B

Task B 等待数据库
       ↓
Event Loop 处理 Task C
```

因此：

> Agent 后端天然非常适合异步 I/O 模型。

---

# 13. Semaphore

当任务数量非常多时，不能无限并发。

例如：

```python
asyncio.gather(
    *(task(i) for i in range(1000))
)
```

可能造成：

```text
API 限流
连接池耗尽
资源压力
数据库连接耗尽
```

因此使用：

```python
semaphore = asyncio.Semaphore(3)
```

表示：

> 最多允许 3 个任务同时进入受限区域。

重要区分：

```text
Task Count
≠
Max Concurrent
```

例如：

```text
1000 个 Task
+
Semaphore(10)
=
最多 10 个并发进入受限区域
```

实际完成的 `06_semaphore.py` 对 10 个任务使用 `Semaphore(3)`，并通过 `active_count` 验证并发数。 

---

# 14. Timeout

外部服务可能长时间不返回：

```text
1 秒
10 秒
1 分钟
```

因此需要设置超时。

例如：

```python
async with asyncio.timeout(3):
    await slow_task()
```

超过 3 秒就触发超时。

实际实验中，`slow_task()` 设置为等待 5 秒，而超时设置为 3 秒，成功验证了超时机制。 

---

# 15. Cancellation

Cancellation：

> 主动要求一个 Task 停止执行。

例如：

```python
task = asyncio.create_task(slow_task())

await asyncio.sleep(2)

task.cancel()
```

然后：

```python
try:
    await task
except asyncio.CancelledError:
    ...
```

需要注意：

> `cancel()` 是发出取消请求，而不是粗暴地强杀 Python 线程。

---

# 16. Agent 为什么需要 Cancellation？

例如：

```text
用户：
搜索 100 个网页
```

Agent 开始：

```text
Search 1
Search 2
...
Search 100
```

用户突然：

> “取消。”

理想行为：

```text
User Cancel
 ↓
Agent Task.cancel()
 ↓
取消未完成任务
 ↓
释放资源
```

否则后台仍然继续请求，会浪费：

```text
Token
网络
API 配额
CPU
内存
```

---

# 17. Exception Handling

并发任务中可能：

```text
Task A → 成功
Task B → 失败
Task C → 成功
```

可以使用：

```python
await asyncio.gather(
    ...,
    return_exceptions=True,
)
```

让异常作为结果返回。

例如：

```text
[
    "A success",
    ValueError(...),
    "C success"
]
```

这样可以分别处理：

```text
成功任务
失败任务
```

而不是直接让整个聚合操作失败。

你的 `09` 实验正是验证了这种行为。

---

# 18. Retry

Tool 失败不一定代表永久失败。

可能只是：

```text
Timeout
502
503
网络波动
临时连接错误
```

所以可以有限重试：

```text
第一次失败
 ↓
第二次
 ↓
第三次
 ↓
仍失败 → 最终失败
```

---

# 19. 什么错误适合 Retry？

### 适合：

```text
Timeout
502
503
临时网络异常
```

### 通常不适合：

```text
参数错误
权限不足
Tool 不存在
业务逻辑错误
```

核心：

> **不是“失败就重试”，而是“判断这个失败是否可恢复”。**

---

# 20. Exponential Backoff

典型：

```text
第一次失败 → 等 1 秒
第二次失败 → 等 2 秒
第三次失败 → 等 4 秒
```

大致：

```text
delay = base × 2^attempt
```

作用：

> 避免失败后立即连续打击服务器。

---

# 21. Jitter

如果很多客户端同时失败：

```text
12:00:00
1000 个请求同时失败

12:00:02
1000 个请求同时重试
```

可能形成：

> Retry Storm / Thundering Herd

加入 Jitter：

```text
A → 1.7s
B → 2.1s
C → 2.5s
D → 1.9s
```

把重试时间错开。

---

# 22. Agent Tool Executor

Day 2 最重要的综合实践：

```text
Agent
 ↓
Tool Calls
 ↓
Tool Executor
 ↓
Semaphore
 ↓
Timeout
 ↓
Execute
 ↓
Exception
 ↓
Retry
 ↓
Success / Failure
```

实际综合实验中实现了：

```text
Search
Weather
Database
```

以及：

```text
Semaphore(3)
Timeout(5s)
Max Retry = 3
asyncio.gather(..., return_exceptions=True)
```

因此已经从单纯学习 `asyncio`，进入：

> **异步 Agent Tool Runtime 的初步设计。**

---

# 23. Day 2 实际表现

## 已掌握

```text
✅ async def
✅ Coroutine
✅ Task
✅ Event Loop
✅ await
✅ create_task
✅ gather
✅ I/O 并发
✅ Semaphore
✅ Timeout
✅ Cancellation
✅ Exception Handling
✅ return_exceptions
✅ Retry
✅ Agent Tool Executor
```

## 仍需加强

### 1. Retry / Error Classification

当前容易理解成：

```text
失败 → Retry
```

应该进一步升级为：

```text
Error
 ↓
Classify
 ├── Retryable
 ├── Fallback
 ├── Replan
 └── Fatal
```

### 2. Backoff

已经理解指数退避，但代码实验中实际写的是：

```python
i * 2
```

对应：

```text
0s
2s
4s
```

严格意义上不是：

```text
1s
2s
4s
```

需要继续熟悉指数退避与 Jitter。

---

# 24. Day 2 核心知识图

```text
asyncio
│
├── Coroutine
│      ↓
├── Task
│      ↓
├── Event Loop
│      ↓
├── await
│      ↓
├── Concurrent I/O
│
├── Semaphore
│      ↓
│   Concurrency Limit
│
├── Timeout
│      ↓
│   防止无限等待
│
├── Cancellation
│      ↓
│   主动终止任务
│
├── Exception Handling
│      ↓
│   隔离失败
│
└── Retry
       ├── Backoff
       └── Jitter
              ↓
        Agent Tool Executor
```

---

# 25. Day 2 最终毕业标准

```text
✅ 能解释 Coroutine / Task / Event Loop
✅ 理解 await 的执行模型
✅ 理解 async ≠ 并发
✅ 能使用 create_task / gather
✅ 能识别 Event Loop 阻塞
✅ 能使用 Semaphore 控制并发
✅ 能使用 Timeout 防止无限等待
✅ 理解 Cancellation
✅ 能处理并发任务异常
✅ 理解 Retry / Backoff / Jitter
✅ 能设计基础 Agent Tool Executor
```