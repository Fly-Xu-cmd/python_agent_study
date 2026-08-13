
# Day 1：Python 类型系统 + Pydantic

## 1. 学习目标

本阶段的目标不是简单记忆 Python 类型注解，而是建立：

```text
Python 类型系统
    ↓
Type Hint
    ↓
Pydantic Runtime Validation
    ↓
JSON Schema
    ↓
LLM Tool Schema
    ↓
Agent Tool Calling
```

最终理解为什么现代 Python AI 工程中，类型系统和 Pydantic 非常重要。

---

## 2. 核心知识

### 2.1 Python 是动态类型语言

Python 的变量类型在运行时可以发生变化：

```python
age = 22
age = "hello"
```

类型注解：

```python
age: int = 22
```

主要用于：

* IDE
* 静态类型检查器
* 提高代码可读性
* 描述函数和数据结构

需要注意：

> Python 类型注解本身通常不负责运行时数据校验。

因此：

```python
age: int = "hello"
```

不能简单理解为 Python 运行时一定会立即报错。

---

## 3. 常见类型注解

### `list[int]`

表示：

```text
list
└── 元素类型：int
```

例如：

```python
numbers: list[int]
```

---

### `dict[str, int]`

表示：

```text
key   → str
value → int
```

例如：

```python
scores: dict[str, int]
```

---

### `Optional`

现代 Python 更推荐：

```python
str | None
```

它与：

```python
Optional[str]
```

等价。

表示：

```text
值可以是 str
或者 None
```

注意：

> `Optional[str]` 表示允许 `None`，并不意味着字段一定可以省略。

---

### `Union`

传统写法：

```python
Union[int, str]
```

现代写法：

```python
int | str
```

表示一个值可以属于多个类型中的一种。

---

### `Literal`

例如：

```python
Literal["search", "database"]
```

表示：

> 值不是任意字符串，而只能是指定的具体值。

特别适合：

```text
Tool Name
Agent Action
Status
Route
Mode
```

例如：

```python
action: Literal["search", "calculator"]
```

---

## 4. TypedDict

`TypedDict` 用来描述一个 `dict` 应该具有什么结构。

例如：

```python
class User(TypedDict):
    name: str
    age: int
```

核心理解：

> TypedDict 本质上仍然是 dict，主要用于类型描述和静态检查。

它不是一个运行时数据验证框架。

---

## 5. TypedDict vs Pydantic

### TypedDict

更适合：

> 描述一个 dict 应该长什么样。

### Pydantic BaseModel

更适合：

> 真正接收、验证、解析、转换和序列化数据。

对比：

| 能力                | TypedDict | Pydantic |
| ----------------- | --------- | -------- |
| 描述数据结构            | ✅         | ✅        |
| 静态类型检查            | ✅         | ✅        |
| 运行时验证             | ❌         | ✅        |
| 数据转换              | ❌         | ✅        |
| JSON Schema       | 不作为主要能力   | ✅        |
| API 数据验证          | 不适合作为主要方案 | ✅        |
| Agent Tool Schema | 较弱        | ✅        |

---

# 6. Pydantic

基本模型：

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Pydantic 的核心作用不只是“检查类型”，还包括：

```text
数据
 ↓
Validation
 ↓
Parsing / Conversion
 ↓
Structured Model
 ↓
Serialization
 ↓
JSON Schema
```

---

## 7. Field

可以通过 `Field` 定义约束。

例如：

```python
class Order(BaseModel):
    price: int = Field(ge=0)
```

表示：

```text
price >= 0
```

你实际代码中已经使用了：

```python
price: int = Field(ge=0)
```

以及：

```python
page: int = Field(ge=1)
limit: int = Field(ge=1, le=100)
```

这些代码已经通过实际运行验证。 

---

# 8. JSON Schema

Pydantic 可以根据 Python Model 生成 JSON Schema：

```python
User.model_json_schema()
```

核心转换关系：

```text
Python Type
    ↓
Pydantic Model
    ↓
JSON Schema
```

Schema 中可以描述：

```text
type
properties
required
enum
minimum
maximum
```

你实际已经成功生成：

```python
User.model_json_schema()
Order.model_json_schema()
ToolArgs.model_json_schema()
```

说明这一部分已经完成实际验证。

---

# 9. 为什么 JSON Schema 与 Agent 有关

假设存在：

```python
search(city: str, page: int)
```

LLM 需要知道：

```text
Tool 名字
参数名称
参数类型
哪些参数必填
参数结构
参数约束
```

因此可以通过 Schema 给模型提供一个结构化的“参数契约”。

核心链路：

```text
Python Function
      ↓
Pydantic Model
      ↓
JSON Schema
      ↓
Tool Schema
      ↓
LLM Tool Calling
```

需要特别理解：

> Schema 本身不是工具能力。

它只是告诉 LLM：

> “这个工具是什么、怎么调用、需要什么参数。”

---

# 10. Tool Calling 的关键认知

LLM 并没有真正执行 Python 函数。

完整过程是：

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Backend
 ↓
Python Function
 ↓
Tool Result
 ↓
LLM
 ↓
Final Answer
```

例如：

```text
LLM
 ↓
{"name": "search", "arguments": {...}}
 ↓
后端解析
 ↓
真正执行 search()
 ↓
返回 Tool Result
 ↓
LLM 继续处理
```

因此：

> **LLM 负责决定“要不要调用什么工具”，真正执行工具的是你的程序。**

这是后续学习 Agent Loop 的基础。

---

# 11. 本次实践

实际完成了以下 Model：

```text
User
Order
ToolArgs
ToolResult
SearchArgs
```

其中：

```python
class Order(BaseModel):
    id: int
    user_id: int
    status: Literal["pending", "paid", "cancelled"]
    price: int = Field(ge=0)
```

以及：

```python
class ToolArgs(BaseModel):
    tool_name: Literal["search", "database", "calculator"]
    query: dict[str, str]
    top_k: int = Field(ge=1)
```



并完成了 JSON Schema 生成。

---

# 12. 本次表现评价

## 已掌握

### ✅ Python 动态类型

已经理解：

> 类型注解不等于运行时类型检查。

### ✅ Optional / Union

能够正确理解：

```python
Optional[str]
```

与：

```python
str | None
```

的关系。

### ✅ Literal

已经理解：

> `str` 是类型范围，`Literal` 是具体允许值集合。

### ✅ TypedDict / Pydantic

已经能够区分：

```text
TypedDict
→ 描述结构

Pydantic
→ 运行时验证 + 数据处理
```

### ✅ Field

能够实际定义：

```text
ge
le
```

等约束。

### ✅ JSON Schema

已经完成实际代码验证。

### ✅ Tool Calling

已经理解：

> LLM 不负责真正执行 Python Tool。

这是今天非常重要的学习成果。

---

# 13. 本次暴露出的薄弱点

## ⚠️ 1. Pydantic 的能力理解得还不够完整

目前更容易把：

> Pydantic = 类型检查

需要进一步建立：

```text
Validation
Parsing
Conversion
Serialization
Schema Generation
```

这一整套认知。

---

## ⚠️ 2. Schema 的核心作用还需要继续深化

目前已经知道：

> Schema 结构化、方便 LLM 理解。

下一步应该深入：

> **Schema 为什么可以成为 Tool Calling 的“契约”？**

尤其需要理解：

```text
Function
Argument Schema
Tool Definition
Tool Call
Tool Result
```

之间的关系。

---

## ⚠️ 3. `nullable` 与 `required` 的区别

例如：

```python
email: str | None
```

意味着：

```text
允许 None
```

但不代表：

```text
允许不传
```

如果希望字段可以省略：

```python
email: str | None = None
```

这是本次额外发现的重要知识点。

---

# 14. Day 1 知识总图

```text
Python
│
├── 动态类型
│
├── Type Hint
│   ├── list[int]
│   ├── dict[str, int]
│   ├── Optional
│   ├── Union
│   ├── Literal
│   ├── TypedDict
│   ├── TypeVar
│   ├── Generic
│   └── Protocol
│
└── Runtime Validation
    │
    └── Pydantic
        ├── BaseModel
        ├── Field
        ├── Validation
        ├── Serialization
        └── JSON Schema
                ↓
           Tool Schema
                ↓
         Tool Calling
                ↓
             Agent
```

---

# 15. Day 1 毕业状态

```text
理论理解       ✅
代码实现       ✅
实际运行       ✅
JSON Schema    ✅
Agent 关联     ✅
核心概念掌握   ✅
细节深度       🟡
```