from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    id: int
    name: str
    age: int
    email: str | None


class Order(BaseModel):
    id: int
    user_id: int
    status: Literal["pending", "paid", "cancelled"]
    price: int = Field(ge=0, description="Price must be greater than or equal to zero")


class ToolArgs(BaseModel):
    tool_name: Literal["search", "database", "calculator"]
    query: dict[str, str]
    top_k: int = Field(ge=1, description="top_k must be greater than or equal to 1")


class ToolResult(BaseModel):
    success: bool
    data: dict[str, str] | None
    error: dict[str, str] | None


user = User(id=1, name="Alice", age=18, email=None)
order = Order(id=1, user_id=1, status="pending", price=100)
tool_args = ToolArgs(tool_name="search", query={"q": "hello"}, top_k=1)

print(User.model_json_schema())
print(Order.model_json_schema())
print(ToolArgs.model_json_schema())


class SearchArgs(BaseModel):
    keyword: str
    page: int = Field(
        ge=1, description="Page number must be greater than or equal to 1"
    )
    limit: int = Field(
        ge=1,
        le=100,
        description="Limit must be greater than or equal to 1 and less than or equal to 100",
    )
