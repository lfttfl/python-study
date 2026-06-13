# Python 类型注解（Type Hints）
# =====================================================
# Python 是动态类型语言，类型注解不影响运行时行为，
# 但能让 IDE 智能提示更准确、mypy 静态检查发现潜在 bug、代码可读性更高。
# Python 3.9+ 内置集合类型支持直接用作注解（list[int] 而非 List[int]）
# Python 3.10+ 支持 X | Y 写法（而非 Union[X, Y]）

from __future__ import annotations              # 让所有注解延迟求值（兼容前向引用）

from typing import (
    Any, Optional, Union, Final, Literal,
    Callable, TypeVar, Generic,
    TypedDict, Protocol, overload,
    NamedTuple, cast, TYPE_CHECKING,
)
import sys

# ══════════════════════════════════════════════════════
# 一、基础类型注解
# ══════════════════════════════════════════════════════

print("══ 一、基础类型注解 ══")

# ── 变量注解 ──
name:   str   = "小明"
age:    int   = 18
height: float = 1.75
active: bool  = True

# 注解不赋值：声明变量存在（类型检查器会用到，运行时无效果）
score: float   # 只声明类型，不赋值

# ── 函数参数和返回值注解 ──
def greet(name: str, times: int = 1) -> str:
    return (f"你好，{name}！" * times).strip()

def add(x: int, y: int) -> int:
    return x + y

def nothing() -> None:                         # 无返回值用 None
    print("无返回值")

print(greet("小明", 2))
print(f"add(1, 2) = {add(1, 2)}")

# ── Python 3.9+ 内置集合类型直接用 ──
def process(items: list[int]) -> dict[str, int]:
    return {"sum": sum(items), "count": len(items)}

def get_pairs() -> list[tuple[str, int]]:
    return [("a", 1), ("b", 2)]

print(process([1, 2, 3]))

# ══════════════════════════════════════════════════════
# 二、Optional 与 Union
# ══════════════════════════════════════════════════════

print("\n══ 二、Optional 与 Union ══")

# Optional[X] 等价于 Union[X, None]，表示"可能是 X 也可能是 None"
def find_user(user_id: int) -> Optional[str]:  # 找到返回名字，找不到返回 None
    db = {1: "Alice", 2: "Bob"}
    return db.get(user_id)

result = find_user(1)
if result is not None:                         # 类型缩窄（type narrowing）
    print(result.upper())                      # 这里 mypy 知道 result 是 str

# Python 3.10+ 写法：X | None 代替 Optional[X]
def find_user_v2(user_id: int) -> str | None:  # 更简洁
    return {1: "Alice"}.get(user_id)

# Union[X, Y]：可以是 X 或 Y 类型之一
def stringify(value: Union[int, float, str]) -> str:
    return str(value)

# Python 3.10+ 写法
def stringify_v2(value: int | float | str) -> str:
    return str(value)

print(stringify(42), stringify(3.14), stringify("hello"))

# ── 类型缩窄（Type Narrowing）──
print("\n── 类型缩窄 ──")

def process_value(value: int | str | list[int]) -> str:
    if isinstance(value, int):
        return f"整数：{value * 2}"           # 这里 mypy 知道 value 是 int
    elif isinstance(value, str):
        return f"字符串：{value.upper()}"     # 这里 value 是 str
    else:
        return f"列表：{sum(value)}"          # 这里 value 是 list[int]

print(process_value(5))
print(process_value("hello"))
print(process_value([1, 2, 3]))

# ══════════════════════════════════════════════════════
# 三、Callable：函数类型
# ══════════════════════════════════════════════════════

print("\n══ 三、Callable ══")

# Callable[[参数类型, ...], 返回类型]
from typing import Callable

def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

def apply_two(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def apply_any(func: Callable[..., Any], *args: Any) -> Any:
    return func(*args)                         # Callable[..., Any]：接受任意参数的函数

double: Callable[[int], int] = lambda x: x * 2
print(apply(double, 5))                        # 10
print(apply_two(lambda a, b: a + b, 3, 4))    # 7

# 高阶函数的注解
def make_multiplier(factor: int) -> Callable[[int], int]:
    return lambda x: x * factor               # 返回值本身也是函数

triple = make_multiplier(3)
print(triple(7))                               # 21

# ══════════════════════════════════════════════════════
# 四、TypeVar 与泛型
# ══════════════════════════════════════════════════════

print("\n══ 四、TypeVar 与泛型 ══")

# TypeVar：定义类型变量，使函数/类能对多种类型通用（泛型）
T = TypeVar("T")                               # 无约束类型变量
N = TypeVar("N", int, float)                  # 受约束：只能是 int 或 float
C = TypeVar("C", bound="Comparable")          # bound：必须是 Comparable 的子类型

# 泛型函数：返回类型与输入类型一致（类型安全的 identity）
def first(items: list[T]) -> T:               # T 在调用时被推断为具体类型
    return items[0]

def clamp(value: N, lo: N, hi: N) -> N:       # N 约束为数值类型
    return max(lo, min(value, hi))

print(first([1, 2, 3]))                        # int → T 被推断为 int
print(first(["a", "b"]))                       # str → T 被推断为 str
print(clamp(15, 0, 10))                        # 10（int）
print(clamp(3.5, 0.0, 5.0))                   # 3.5（float）

# ── 泛型类 ──
print("\n── 泛型类 ──")

class Stack(Generic[T]):                       # Generic[T] 声明这是泛型类
    """类型安全的栈"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("栈为空")
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"


int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
print(f"栈：{int_stack}")
print(f"弹出：{int_stack.pop()}")              # 3

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
print(f"字符串栈：{str_stack}")

# ══════════════════════════════════════════════════════
# 五、TypedDict：有类型的字典
# ══════════════════════════════════════════════════════

print("\n══ 五、TypedDict ══")

# TypedDict：定义字典的"形状"，每个键的类型都固定
# 比 dict[str, Any] 更精确，比 dataclass 更轻量（无需实例化）

class UserInfo(TypedDict):
    name:  str
    age:   int
    email: str

class UserInfoPartial(TypedDict, total=False):  # total=False：所有键都是可选的
    nickname: str
    avatar:   str

# 使用
user: UserInfo = {"name": "小明", "age": 18, "email": "xm@mail.com"}
print(f"用户：{user['name']}，{user['age']}岁")

# TypedDict 可以继承
class AdminInfo(UserInfo):
    role:        str
    permissions: list[str]

admin: AdminInfo = {
    "name": "Admin", "age": 30, "email": "admin@mail.com",
    "role": "superadmin", "permissions": ["read", "write", "delete"]
}
print(f"管理员：{admin['name']}，权限：{admin['permissions']}")

# ══════════════════════════════════════════════════════
# 六、Protocol：结构子类型（鸭子类型的类型化）
# ══════════════════════════════════════════════════════

print("\n══ 六、Protocol（鸭子类型） ══")

# Protocol：定义"有哪些方法/属性就符合这个类型"
# 不需要显式继承，只要结构匹配就满足（structural subtyping）

class Drawable(Protocol):
    def draw(self) -> str: ...                 # ... 是方法体占位符（Protocol 里常见）

class Sizeable(Protocol):
    def __len__(self) -> int: ...

class DrawableAndSizeable(Drawable, Sizeable, Protocol):  # 组合协议
    ...


# 这些类没有继承 Drawable，但实现了 draw 方法
class Circle:
    def __init__(self, r: float):
        self.r = r
    def draw(self) -> str:
        return f"○ 圆（半径={self.r}）"

class Square:
    def __init__(self, side: float):
        self.side = side
    def draw(self) -> str:
        return f"□ 正方形（边长={self.side}）"


def render(shape: Drawable) -> None:           # 接受任何有 draw 方法的对象
    print(f"  渲染：{shape.draw()}")

shapes: list[Drawable] = [Circle(5), Square(3)]
for s in shapes:
    render(s)

# ── runtime_checkable：让 Protocol 支持 isinstance 检查 ──
from typing import runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

class FileWrapper:
    def close(self) -> None:
        print("  [关闭文件]")

fw = FileWrapper()
print(f"FileWrapper 实现了 Closeable：{isinstance(fw, Closeable)}")  # True

# ══════════════════════════════════════════════════════
# 七、Literal、Final、overload
# ══════════════════════════════════════════════════════

print("\n══ 七、Literal / Final / overload ══")

# ── Literal：限制参数只能是特定值 ──
print("\n── Literal ──")

Direction = Literal["north", "south", "east", "west"]

def move(direction: Direction, steps: int) -> str:
    return f"向{direction}走{steps}步"

print(move("north", 3))
# move("up", 1)  # mypy 会报错：'up' 不在 Literal 的范围内

# Literal 用于函数重载的区分
def open_file(path: str, mode: Literal["r", "w", "rb", "wb"]) -> str:
    return f"以 {mode} 模式打开 {path}"

print(open_file("data.txt", "r"))

# ── Final：不可重新赋值的常量 ──
print("\n── Final ──")

MAX_RETRY:  Final = 3
API_URL:    Final[str] = "https://api.example.com"
PI:         Final = 3.14159265358979

print(f"MAX_RETRY = {MAX_RETRY}")
# MAX_RETRY = 5  # mypy 会报错：不能给 Final 变量重新赋值

# Final 类变量：子类不能重写
class Config:
    DEBUG: Final = False
    VERSION: Final[str] = "1.0.0"

# ── overload：同一函数名的多个签名 ──
print("\n── overload ──")

# @overload 声明不同的输入/输出类型组合，实际实现只有最后一个（不带 @overload）
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
@overload
def double(x: list[T]) -> list[T]: ...        # type: ignore[misc]

def double(x):                                 # 实际实现
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x * 2
    elif isinstance(x, list):
        return x * 2
    raise TypeError(f"不支持的类型：{type(x)}")

print(double(5))                               # 10（int）
print(double("hi"))                            # hihi（str）
print(double([1, 2]))                          # [1, 2, 1, 2]（list）

# ══════════════════════════════════════════════════════
# 八、NamedTuple：带类型的命名元组
# ══════════════════════════════════════════════════════

print("\n══ 八、NamedTuple ══")

# typing.NamedTuple：比 collections.namedtuple 更现代，支持类型注解和默认值

class Point(NamedTuple):
    x: float
    y: float
    z: float = 0.0                             # 有默认值的字段

    def distance_to_origin(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

p1 = Point(3.0, 4.0)
p2 = Point(1.0, 2.0, 3.0)

print(f"p1 = {p1}")
print(f"p1 到原点距离：{p1.distance_to_origin():.2f}")  # 5.0
print(f"p1 == Point(3,4)：{p1 == Point(3.0, 4.0)}")    # True
print(f"p1 是元组：{isinstance(p1, tuple)}")             # True（NamedTuple 是元组子类）

# ══════════════════════════════════════════════════════
# 九、cast 与 TYPE_CHECKING
# ══════════════════════════════════════════════════════

print("\n══ 九、cast 与 TYPE_CHECKING ══")

# cast(Type, value)：告诉类型检查器"我确定这个值的类型是 Type"
# 运行时什么都不做（直接返回 value），纯粹给静态检查器看

def get_config_value(key: str) -> Any:
    config = {"port": 8080, "host": "localhost"}
    return config.get(key)

port = cast(int, get_config_value("port"))     # 告诉 mypy：port 是 int
print(f"端口：{port + 1}")                      # mypy 不会报 int + 1 的类型错误

# TYPE_CHECKING：只在类型检查时为 True，运行时为 False
# 用于避免循环导入（import 只在类型检查时执行，运行时不执行）
if TYPE_CHECKING:
    from pathlib import Path                   # 假设这里可能有循环导入

def read_lines(path: Path) -> list[str]:       # Path 在运行时不会被实际导入
    from pathlib import Path as _Path          # 运行时从这里导入
    return _Path(path).read_text().splitlines()

# ══════════════════════════════════════════════════════
# 十、综合示例：类型安全的数据处理管道
# ══════════════════════════════════════════════════════

print("\n══ 十、综合示例：类型安全的管道 ══")

from typing import Iterator

class Record(TypedDict):
    name:  str
    score: float
    grade: str

def parse_record(raw: dict[str, str]) -> Optional[Record]:
    """把原始字符串字典解析为类型化 Record，失败返回 None"""
    try:
        score = float(raw["score"])
        grade = "优" if score >= 90 else "良" if score >= 75 else "及格" if score >= 60 else "不及格"
        return Record(name=raw["name"].strip(), score=score, grade=grade)
    except (KeyError, ValueError):
        return None

def filter_passing(records: Iterator[Record]) -> Iterator[Record]:
    return (r for r in records if r["score"] >= 60)

def top_n(records: list[Record], n: int) -> list[Record]:
    return sorted(records, key=lambda r: r["score"], reverse=True)[:n]

raw_data: list[dict[str, str]] = [
    {"name": "  小明 ", "score": "88"},
    {"name": "小红",    "score": "95"},
    {"name": "小刚",    "score": "invalid"},
    {"name": "小李",    "score": "45"},
    {"name": "小王",    "score": "72"},
]

parsed:  list[Record] = [r for raw in raw_data if (r := parse_record(raw)) is not None]
passing: list[Record] = list(filter_passing(iter(parsed)))
top3:    list[Record] = top_n(passing, 3)

print(f"{'姓名':<6}{'分数':>6}{'等级':>6}")
print("-" * 20)
for r in top3:
    print(f"{r['name']:<6}{r['score']:>6.1f}{r['grade']:>6}")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("\n══ 练习题 ══")
print("""
1. 给以下函数补全完整的类型注解（参数、返回值、局部变量）：
   def process(data, key, default=None):
       if key in data:
           return data[key]
       return default

2. 用 Protocol 定义 Comparable 协议（支持 < 和 == 运算符），
   实现泛型函数 sort_items(items: list[C]) -> list[C]，
   用 TypeVar(bound=Comparable) 约束类型。

3. 用 TypedDict 定义 APIResponse，包含：
   status: int, message: str, data: Optional[dict[str, Any]]
   写函数 parse_response(raw: dict) -> APIResponse，
   并处理缺少键或类型不匹配的情况。

4. 给 Stack[T]（本文件的泛型类）补全以下方法的类型注解：
   - __iter__：返回 Iterator[T]
   - __contains__：接受 object，返回 bool
   - extend(items: Iterable[T]) -> None

参考答案见下方注释：
""")

# # 答案1：
# from typing import TypeVar, Optional
# KT = TypeVar("KT")
# VT = TypeVar("VT")
# def process(data: dict[KT, VT], key: KT, default: Optional[VT] = None) -> Optional[VT]:
#     if key in data:
#         return data[key]
#     return default
#
# # 答案2：
# from typing import Protocol, TypeVar, runtime_checkable
# @runtime_checkable
# class Comparable(Protocol):
#     def __lt__(self, other: object) -> bool: ...
#     def __eq__(self, other: object) -> bool: ...
# C = TypeVar("C", bound=Comparable)
# def sort_items(items: list[C]) -> list[C]:
#     return sorted(items)
# print(sort_items([3, 1, 4, 1, 5]))   # [1, 1, 3, 4, 5]
# print(sort_items(["banana", "apple", "cherry"]))
