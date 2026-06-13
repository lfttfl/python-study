# Python 面向对象编程：dataclass、property、上下文管理器
# =====================================================

from dataclasses import dataclass, field, KW_ONLY
import dataclasses

# ══════════════════════════════════════════════════════
# 一、@property：受控属性访问
# ══════════════════════════════════════════════════════

print("══ 一、@property ══")

# @property 把方法变成"属性式访问"，可以在读/写/删时加入验证或计算逻辑
# 相比直接暴露实例变量，提供了更好的封装

class Temperature:
    """温度类：用 property 保证摄氏度值在合理范围，并按需提供华氏度转换"""

    ABSOLUTE_ZERO = -273.15                    # 绝对零度（摄氏）

    def __init__(self, celsius):
        self.celsius = celsius                 # 通过 setter 赋值，触发验证

    @property
    def celsius(self):                         # getter：访问 t.celsius 时调用
        return self._celsius                   # 真实值存在 _celsius（约定私有）

    @celsius.setter
    def celsius(self, value):                  # setter：赋值 t.celsius = x 时调用
        if value < Temperature.ABSOLUTE_ZERO:
            raise ValueError(f"温度不能低于绝对零度 {Temperature.ABSOLUTE_ZERO}°C")
        self._celsius = value                  # 通过验证才真正存储

    @celsius.deleter
    def celsius(self):                         # deleter：del t.celsius 时调用（可选）
        raise AttributeError("不允许删除温度属性")

    @property
    def fahrenheit(self):                      # 计算属性：从 celsius 推导，无需存储
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):               # 允许直接用华氏度设置
        self.celsius = (value - 32) * 5 / 9   # 转换后调用 celsius setter（含验证）

    @property
    def kelvin(self):
        return self._celsius - Temperature.ABSOLUTE_ZERO

    def __repr__(self):
        return f"Temperature({self._celsius}°C)"


t = Temperature(100)
print(f"摄氏：{t.celsius}°C")
print(f"华氏：{t.fahrenheit}°F")              # 212.0
print(f"开尔文：{t.kelvin:.2f}K")             # 373.15

t.celsius = 0                                  # setter 触发，正常赋值
print(f"更新后：{t.celsius}°C = {t.fahrenheit}°F")

t.fahrenheit = 212                             # 通过 fahrenheit setter 设置
print(f"华氏 212 对应：{t.celsius}°C")        # 100.0

try:
    t.celsius = -300                           # 低于绝对零度，setter 拒绝
except ValueError as e:
    print(f"验证失败：{e}")

# ── 只读属性 ──
print("\n── 只读属性 ──")

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value

    @property
    def area(self):                            # 只有 getter，没有 setter → 只读属性
        import math
        return math.pi * self._radius ** 2

    @property
    def diameter(self):
        return self._radius * 2


c = Circle(5)
print(f"半径={c.radius}, 直径={c.diameter}, 面积={c.area:.2f}")

try:
    c.area = 100                               # 只读属性，没有 setter，报 AttributeError
except AttributeError as e:
    print(f"只读属性不可赋值：{e}")

# ══════════════════════════════════════════════════════
# 二、@dataclass：自动生成样板代码
# ══════════════════════════════════════════════════════

print("\n══ 二、@dataclass ══")

# @dataclass 根据类型注解自动生成 __init__、__repr__、__eq__ 等方法
# 大幅减少数据类（主要用于存储数据的类）的样板代码

# ── 基础用法 ──
@dataclass
class Point:
    x: float                                   # 字段：用类型注解声明
    y: float
    z: float = 0.0                             # 有默认值的字段必须在没有默认值的字段之后

p1 = Point(1.0, 2.0)
p2 = Point(3.0, 4.0, 5.0)
p3 = Point(1.0, 2.0)

print(f"p1 = {p1}")                            # Point(x=1.0, y=2.0, z=0.0)，自动 __repr__
print(f"p1 == p3：{p1 == p3}")                 # True，自动 __eq__（按字段逐一比较）
print(f"p1 == p2：{p1 == p2}")                 # False

# ── 常用参数 ──
print("\n── dataclass 参数 ──")

@dataclass(order=True, frozen=True)            # order=True：生成比较运算符；frozen=True：不可变
class Version:
    major: int
    minor: int = 0
    patch: int = 0

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

v1 = Version(2, 1, 0)
v2 = Version(2, 0, 5)
v3 = Version(3)

print(f"{v1} < {v3}：{v1 < v3}")              # True（先比较 major）
print(f"{v1} > {v2}：{v1 > v2}")              # True（major 相同比 minor）
print(sorted([v3, v1, v2]))                    # [v2.0.5, v2.1.0, v3.0.0]

try:
    v1.major = 4                               # frozen=True，不可修改
except dataclasses.FrozenInstanceError as e:
    print(f"frozen 不可修改：{e}")

# frozen=True 的 dataclass 可以哈希，可以放入集合
v_set = {v1, v2, v3, Version(2, 1, 0)}        # v1 和 Version(2,1,0) 相等，去重
print(f"版本集合：{v_set}")

# ── field()：精细控制每个字段 ──
print("\n── field() 控制字段 ──")

@dataclass
class Student:
    name:    str
    score:   float
    courses: list = field(default_factory=list)  # 可变类型必须用 default_factory，不能直接写 []
    _id:     int  = field(default=0, repr=False, compare=False)  # repr=False 不在 __repr__ 里显示

    def enroll(self, course):
        self.courses.append(course)
        return self

    def __post_init__(self):                   # 实例化后自动调用，可做后处理或验证
        if not (0 <= self.score <= 100):
            raise ValueError(f"成绩 {self.score} 不合法")
        self.name = self.name.strip()          # 清理空白

s1 = Student("小明", 88)
s2 = Student("小红", 92)
s1.enroll("数学").enroll("英语")

print(s1)                                      # Student(name='小明', score=88, courses=['数学', '英语'])
print(f"s1 == s2：{s1 == s2}")                 # False

try:
    Student("test", 105)
except ValueError as e:
    print(f"后处理验证：{e}")

# ── dataclass 继承 ──
print("\n── dataclass 继承 ──")

@dataclass
class Person:
    name: str
    age:  int

@dataclass
class Employee(Person):
    company:  str
    salary:   float = 0.0

    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("薪资不能为负")

emp = Employee("小李", 30, "字节跳动", 25000)
print(emp)                                     # Employee(name='小李', age=30, company='字节跳动', salary=25000)

# asdict / astuple：转换为字典或元组（方便序列化）
print(dataclasses.asdict(emp))
print(dataclasses.astuple(emp))

# replace：基于现有实例创建修改了部分字段的新实例（类似 namedtuple._replace）
emp2 = dataclasses.replace(emp, salary=30000)
print(f"涨薪后：{emp2}")

# ══════════════════════════════════════════════════════
# 三、上下文管理器（Context Manager）
# ══════════════════════════════════════════════════════

print("\n══ 三、上下文管理器 ══")

# with 语句保证资源（文件、连接、锁）的正确获取和释放，即使发生异常也不例外
# 背后调用 __enter__（进入 with 块）和 __exit__（退出 with 块，无论是否异常）

# ── 方式一：实现 __enter__ 和 __exit__ ──
print("\n── 类实现上下文管理器 ──")

class Timer:
    """计时上下文管理器：测量 with 块的执行时间"""
    import time as _time

    def __init__(self, name=""):
        self.name    = name
        self.elapsed = 0.0

    def __enter__(self):                       # 进入 with 块时调用，返回值绑定到 as 变量
        import time
        self._start = time.perf_counter()
        return self                            # 返回 self，让 as 可以访问 timer.elapsed

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type/val/tb：异常信息，没有异常则全为 None
        # 返回 True：吞掉异常（慎用）；返回 False/None：异常正常传播
        import time
        self.elapsed = time.perf_counter() - self._start
        print(f"[Timer] {self.name or '代码块'} 耗时：{self.elapsed:.6f} 秒")
        return False                           # 不吞掉异常

with Timer("列表生成") as t:
    result = [i ** 2 for i in range(100_000)]
print(f"计时结果：{t.elapsed:.6f} 秒")

# ── 上下文管理器处理异常 ──
print("\n── 异常处理 ──")

class ManagedResource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"  [获取] {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [释放] {self.name}（异常：{exc_type.__name__ if exc_type else '无'}）")
        return False                           # 不吞异常，让调用方处理

print("正常情况：")
with ManagedResource("数据库连接") as res:
    print(f"  [使用] {res.name}")

print("\n有异常：")
try:
    with ManagedResource("文件句柄") as res:
        print(f"  [使用] {res.name}")
        raise RuntimeError("模拟错误")        # 异常也能触发 __exit__
except RuntimeError:
    print("  [捕获] 异常被外层处理")

# ── 方式二：用 contextlib.contextmanager 装饰生成器函数 ──
print("\n── contextmanager 装饰器 ──")

from contextlib import contextmanager, suppress

@contextmanager
def managed_connection(host):
    """用生成器实现上下文管理器：yield 前是 __enter__，yield 后是 __exit__"""
    print(f"  [连接] {host}")
    conn = {"host": host, "status": "connected"}  # 模拟连接对象
    try:
        yield conn                             # yield 的值绑定到 as 变量，暂停执行
    except Exception as e:
        print(f"  [错误] {e}")
        raise                                  # 重新抛出，让调用方处理
    finally:
        conn["status"] = "closed"
        print(f"  [关闭] {host}")              # 无论是否异常都执行

with managed_connection("db.example.com") as conn:
    print(f"  [查询] 使用连接：{conn}")

# suppress：忽略特定类型的异常（contextlib 提供的实用上下文管理器）
print("\n── suppress 忽略异常 ──")
with suppress(FileNotFoundError):
    open("不存在的文件.txt")                   # 不会抛出，异常被静默忽略
print("文件不存在但程序继续运行")

# ── 嵌套上下文管理器 ──
print("\n── 嵌套 with ──")

# 多个 with 可以合并写
with Timer("双计时") as outer, managed_connection("api.example.com") as conn:
    _ = [i * 2 for i in range(50_000)]

# ══════════════════════════════════════════════════════
# 四、综合示例：配置管理器
# ══════════════════════════════════════════════════════

print("\n══ 四、综合示例：配置管理器 ══")

@dataclass
class DBConfig:
    host:     str = "localhost"
    port:     int = 5432
    database: str = "mydb"
    username: str = "admin"
    password: str = field(default="", repr=False)  # 密码不显示在 repr 中

    def __post_init__(self):
        if not (1 <= self.port <= 65535):
            raise ValueError(f"端口号 {self.port} 不合法")

    @property
    def dsn(self):
        return f"postgresql://{self.username}@{self.host}:{self.port}/{self.database}"


class DatabaseSession:
    """数据库会话，作为上下文管理器使用"""

    def __init__(self, config: DBConfig):
        self.config = config
        self._conn  = None
        self.query_count = 0

    def __enter__(self):
        print(f"  [连接] DSN: {self.config.dsn}")
        self._conn = {"dsn": self.config.dsn, "open": True}
        return self

    def query(self, sql):
        if not self._conn or not self._conn["open"]:
            raise RuntimeError("连接已关闭")
        self.query_count += 1
        print(f"  [查询#{self.query_count}] {sql}")
        return [{"id": i, "value": i * 10} for i in range(3)]  # 模拟结果

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn["open"] = False
        status = "回滚" if exc_type else "提交"
        print(f"  [{status}] 事务结束，共执行 {self.query_count} 条查询")
        return False


config = DBConfig(host="prod-db.internal", port=5432, database="users", password="secret")
print(f"配置：{config}")
print(f"DSN：{config.dsn}")

with DatabaseSession(config) as db:
    users    = db.query("SELECT * FROM users LIMIT 10")
    admins   = db.query("SELECT * FROM users WHERE role='admin'")
    print(f"  查询结果：{len(users)} 条用户")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("\n══ 练习题 ══")
print("""
1. 用 @dataclass 定义 Product（商品）类：name、price（用 property 验证 >0）、
   quantity（用 property 验证 >=0）。实现 total_value 计算属性（= price * quantity）。

2. 实现上下文管理器 AtomicWrite(path)：
   - __enter__ 返回一个临时文件对象
   - __exit__ 成功时把临时文件改名为目标路径，失败时删除临时文件
   （提示：用 tempfile.NamedTemporaryFile 和 os.replace）

3. 定义 @dataclass LogEntry：timestamp（自动填充当前时间）、level、message。
   添加 @classmethod from_string(cls, line) 解析 "2024-01-01 INFO message" 格式的字符串。

参考答案见下方注释：
""")

# # 答案1：
# @dataclass
# class Product:
#     name:     str
#     _price:   float = field(default=0.0, repr=False)
#     _quantity: int  = field(default=0,   repr=False)
#
#     @property
#     def price(self):       return self._price
#     @price.setter
#     def price(self, v):
#         if v <= 0: raise ValueError("价格必须大于 0")
#         self._price = v
#
#     @property
#     def quantity(self):    return self._quantity
#     @quantity.setter
#     def quantity(self, v):
#         if v < 0: raise ValueError("数量不能为负")
#         self._quantity = v
#
#     @property
#     def total_value(self): return self._price * self._quantity
