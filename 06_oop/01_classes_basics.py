# Python 面向对象编程：类基础
# =====================================================

# ══════════════════════════════════════════════════════
# 一、类与实例
# ══════════════════════════════════════════════════════

print("══ 一、类与实例 ══")

# class 关键字定义类，类名用大驼峰（PascalCase）
# 类是"模板"，实例是根据模板创建的具体对象
class Dog:
    """狗类：演示类的基本结构"""

    species = "Canis lupus familiaris"          # 类变量：所有实例共享，定义在方法外

    def __init__(self, name, age):              # __init__：实例初始化方法，第一个参数固定是 self
        self.name = name                        # 实例变量：每个实例独立存储，通过 self 访问
        self.age  = age                         # self 代表"当前实例"，类似其他语言的 this

    def bark(self):                             # 实例方法：第一个参数固定是 self
        return f"{self.name} 说：汪！"

    def describe(self):
        return f"{self.name}，{self.age}岁，物种：{Dog.species}"

dog1 = Dog("旺财", 3)                          # 创建实例：自动调用 __init__，不用传 self
dog2 = Dog("球球", 5)

print(dog1.bark())                              # 旺财 说：汪！
print(dog2.describe())                          # 球球，5岁，物种：Canis lupus familiaris

# 实例变量独立，类变量共享
print(dog1.name, dog2.name)                     # 旺财 球球（各自独立）
print(dog1.species, dog2.species)               # 同一类变量

# 修改类变量：通过类名修改影响所有实例，通过实例名修改只影响该实例（会创建同名实例变量）
Dog.species = "Dog"                             # 通过类名修改：影响所有实例
print(dog1.species, dog2.species)               # Dog Dog

dog1.species = "Puppy"                          # 通过实例修改：只给 dog1 创建了实例变量
print(dog1.species, dog2.species)               # Puppy Dog（dog1 的实例变量遮蔽了类变量）

# ── 类变量 vs 实例变量 ──
print("\n── 类变量 vs 实例变量 ──")

class Counter:
    count = 0                                   # 类变量：记录创建了多少个实例

    def __init__(self, name):
        Counter.count += 1                      # 修改类变量用 类名.变量，不要用 self
        self.id   = Counter.count               # 实例变量：本实例的编号
        self.name = name

    def __repr__(self):
        return f"Counter({self.id}: {self.name})"

a = Counter("A")
b = Counter("B")
c = Counter("C")
print(f"共创建了 {Counter.count} 个实例：{a}, {b}, {c}")

# ══════════════════════════════════════════════════════
# 二、魔法方法（Dunder Methods）
# ══════════════════════════════════════════════════════

print("\n══ 二、魔法方法 ══")

# 魔法方法（双下划线开头和结尾）让自定义类支持内置运算符和函数
# 实现魔法方法 = 让对象"表现得像内置类型"

class Vector:
    """二维向量，演示常用魔法方法"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # ── 字符串表示 ──
    def __repr__(self):
        # __repr__：面向开发者的表示，目标是"准确且可重现"
        # eval(repr(obj)) 理想情况下应该能重建对象
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        # __str__：面向用户的表示，目标是"可读"
        # print() 和 str() 优先调用 __str__，没有时回落到 __repr__
        return f"({self.x}, {self.y})"

    # ── 算术运算符 ──
    def __add__(self, other):                   # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):                   # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):                  # v * 3（标量乘法）
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):                 # 3 * v（右乘，左操作数不支持时调用）
        return self.__mul__(scalar)

    def __neg__(self):                          # -v（取负）
        return Vector(-self.x, -self.y)

    # ── 比较运算符 ──
    def __eq__(self, other):                    # v1 == v2
        if not isinstance(other, Vector):       # 类型检查，防止与非向量比较
            return NotImplemented               # 返回 NotImplemented 让 Python 尝试反向操作
        return self.x == other.x and self.y == other.y

    def __hash__(self):                         # 定义了 __eq__ 后必须也定义 __hash__，否则对象不可哈希
        return hash((self.x, self.y))           # 用元组的哈希值

    # ── 容器协议 ──
    def __len__(self):                          # len(v)
        return 2                                # 向量有 2 个分量

    def __getitem__(self, index):               # v[0]、v[1]，支持索引访问
        return (self.x, self.y)[index]

    def __iter__(self):                         # for component in v，支持迭代解包
        yield self.x
        yield self.y

    # ── 其他 ──
    def __abs__(self):                          # abs(v)，向量模长
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):                         # bool(v)，零向量为 False
        return self.x != 0 or self.y != 0

print("\n── 向量运算 ──")
v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(f"repr：{repr(v1)}")                      # Vector(1, 2)
print(f"str： {v1}")                            # (1, 2)（print 调用 __str__）
print(f"v1 + v2 = {v1 + v2}")                  # (4, 6)
print(f"v1 - v2 = {v1 - v2}")                  # (-2, -2)
print(f"v1 * 3 = {v1 * 3}")                    # (3, 6)
print(f"3 * v1 = {3 * v1}")                    # (3, 6)（__rmul__）
print(f"-v1 = {-v1}")                           # (-1, -2)
print(f"v1 == v1：{v1 == v1}")                  # True
print(f"v1 == v2：{v1 == v2}")                  # False
print(f"abs(v2) = {abs(v2):.2f}")               # 5.00（勾股定理）
print(f"len(v1) = {len(v1)}")                   # 2
print(f"v1[0], v1[1] = {v1[0]}, {v1[1]}")      # 1, 2
x, y = v1                                       # __iter__ 支持解包
print(f"解包：x={x}, y={y}")
print(f"bool(v1)={bool(v1)}, bool(Vector(0,0))={bool(Vector(0,0))}")

# 可以放入集合和字典（因为实现了 __hash__）
v_set = {v1, v2, Vector(1, 2)}                 # v1 和 Vector(1,2) 相等，集合只保留一个
print(f"集合去重：{v_set}")                      # 2 个元素

# ══════════════════════════════════════════════════════
# 三、classmethod 与 staticmethod
# ══════════════════════════════════════════════════════

print("\n══ 三、classmethod 与 staticmethod ══")

class Date:
    """日期类，演示 classmethod 和 staticmethod"""

    def __init__(self, year, month, day):
        self.year  = year
        self.month = month
        self.day   = day

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    # ── 实例方法：操作实例数据，第一个参数是 self ──
    def is_leap_year(self):
        y = self.year
        return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

    # ── classmethod：接收类本身而非实例，第一个参数是 cls ──
    # 常用于"工厂方法"：提供除 __init__ 之外的其他构造方式
    @classmethod
    def from_string(cls, date_str):             # cls 是 Date 类本身（或子类）
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)            # 用 cls 而非 Date，子类继承时更正确

    @classmethod
    def today(cls):
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

    # ── staticmethod：不接收 self 或 cls，就是普通函数挂载在类上 ──
    # 逻辑上属于类，但不依赖类或实例的状态
    @staticmethod
    def is_valid_date(year, month, day):
        if month < 1 or month > 12:
            return False
        max_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            max_days[1] = 29                    # 闰年 2 月有 29 天
        return 1 <= day <= max_days[month - 1]

print("── 工厂方法（classmethod）──")
d1 = Date(2024, 6, 15)
d2 = Date.from_string("2024-06-15")            # 从字符串构造
d3 = Date.today()                              # 今天的日期

print(f"直接构造：{d1}")
print(f"from_string：{d2}")
print(f"今天：{d3}")
print(f"2024 是闰年：{d1.is_leap_year()}")      # True（2024能被4整除）

print("\n── 静态方法（staticmethod）──")
print(f"2024-02-29 合法：{Date.is_valid_date(2024, 2, 29)}")   # True（闰年）
print(f"2023-02-29 合法：{Date.is_valid_date(2023, 2, 29)}")   # False（平年）
print(f"2024-13-01 合法：{Date.is_valid_date(2024, 13, 1)}")   # False（月份>12）

# 三者比较
print("\n── 三种方法的对比 ──")
# │ 方法类型      │ 第一参数 │ 能访问实例 │ 能访问类 │ 典型用途              │
# │ 实例方法      │ self     │ ✓          │ ✓        │ 操作实例状态          │
# │ classmethod   │ cls      │ ✗          │ ✓        │ 工厂方法、修改类状态  │
# │ staticmethod  │ 无       │ ✗          │ ✗        │ 工具函数、逻辑归类    │

# ══════════════════════════════════════════════════════
# 四、__slots__：内存优化
# ══════════════════════════════════════════════════════

print("\n══ 四、__slots__ ══")

# 普通类：每个实例有一个 __dict__ 字典存储实例变量，灵活但占内存多
# __slots__：声明允许的实例变量名，禁止 __dict__，显著节省内存（适合大量创建的小对象）

class PointWithDict:                            # 普通类
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointWithSlots:                           # 使用 __slots__
    __slots__ = ("x", "y")                     # 只允许 x 和 y 两个实例变量

    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
p_dict  = PointWithDict(1, 2)
p_slots = PointWithSlots(1, 2)

print(f"普通类内存：{sys.getsizeof(p_dict) + sys.getsizeof(p_dict.__dict__)} 字节")
print(f"__slots__ 内存：{sys.getsizeof(p_slots)} 字节")

# __slots__ 类不能动态添加新属性
try:
    p_slots.z = 3                              # 会抛出 AttributeError
except AttributeError as e:
    print(f"无法添加新属性：{e}")

# ══════════════════════════════════════════════════════
# 五、综合示例：银行账户
# ══════════════════════════════════════════════════════

print("\n══ 五、综合示例：银行账户 ══")

class BankAccount:
    """银行账户：综合演示类的各种特性"""

    _interest_rate = 0.03                      # 约定 _ 前缀表示"类内部使用"（非强制私有）
    _total_accounts = 0

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("初始余额不能为负数")
        self._owner   = owner
        self._balance = balance
        BankAccount._total_accounts += 1
        self._account_id = BankAccount._total_accounts
        self._transactions = []                # 交易历史

    # __repr__ 用于调试，包含所有关键信息
    def __repr__(self):
        return f"BankAccount(owner={self._owner!r}, balance={self._balance})"

    # __str__ 面向用户，简洁可读
    def __str__(self):
        return f"账户#{self._account_id}（{self._owner}）余额：¥{self._balance:,.2f}"

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self._account_id == other._account_id

    def __hash__(self):
        return hash(self._account_id)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于 0")
        self._balance += amount
        self._transactions.append(f"+¥{amount:,.2f}")
        return self                             # 返回 self 支持链式调用

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于 0")
        if amount > self._balance:
            raise ValueError(f"余额不足（当前余额 ¥{self._balance:,.2f}）")
        self._balance -= amount
        self._transactions.append(f"-¥{amount:,.2f}")
        return self

    def apply_interest(self):
        interest = self._balance * BankAccount._interest_rate
        self._balance += interest
        self._transactions.append(f"利息+¥{interest:,.2f}")
        return self

    @property
    def balance(self):                         # @property 让方法像属性一样访问（详见 03 文件）
        return self._balance

    @classmethod
    def set_interest_rate(cls, rate):
        if not (0 <= rate <= 1):
            raise ValueError("利率必须在 0 到 1 之间")
        cls._interest_rate = rate

    @classmethod
    def total_accounts(cls):
        return cls._total_accounts

    def transfer_to(self, target, amount):
        self.withdraw(amount)
        target.deposit(amount)
        return self

acc1 = BankAccount("小明", 1000)
acc2 = BankAccount("小红", 500)

print(acc1)
print(acc2)

# 链式调用：每个方法返回 self
acc1.deposit(500).deposit(300).withdraw(200)
print(f"链式操作后：{acc1}")                    # 1600

# 转账
acc1.transfer_to(acc2, 300)
print(f"转账后：{acc1}")                        # 1300
print(f"转账后：{acc2}")                        # 800

# 应用利息
BankAccount.set_interest_rate(0.05)
acc1.apply_interest()
print(f"利息后：{acc1}")                        # 1365

print(f"总账户数：{BankAccount.total_accounts()}")  # 2
print(f"交易记录：{acc1._transactions}")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("\n══ 练习题 ══")
print("""
1. 定义一个 Rectangle 类，包含 width 和 height 属性，
   实现 area()（面积）、perimeter()（周长）方法，
   以及 __repr__、__eq__（面积相等则认为相等）、__lt__（面积比较）。

2. 为 Rectangle 添加 classmethod from_square(side)，
   用边长创建正方形（即 width == height == side）。

3. 定义一个 Temperature 类，支持摄氏、华氏、开尔文三种温度，
   实现 from_celsius、from_fahrenheit、from_kelvin 三个工厂方法，
   以及转换属性 celsius、fahrenheit、kelvin。

参考答案见下方注释：
""")

# # 答案1 & 2：
# class Rectangle:
#     def __init__(self, width, height):
#         self.width  = width
#         self.height = height
#     def area(self):         return self.width * self.height
#     def perimeter(self):    return 2 * (self.width + self.height)
#     def __repr__(self):     return f"Rectangle({self.width}, {self.height})"
#     def __eq__(self, other): return isinstance(other, Rectangle) and self.area() == other.area()
#     def __hash__(self):     return hash(self.area())
#     def __lt__(self, other): return self.area() < other.area()
#     @classmethod
#     def from_square(cls, side): return cls(side, side)
#
# r1, r2 = Rectangle(3, 4), Rectangle(2, 6)
# print(r1.area(), r1.perimeter())   # 12 14
# print(r1 == r2)                    # True（面积都是 12）
# print(sorted([Rectangle(4,4), r1, Rectangle(1,1)]))
# print(Rectangle.from_square(5))    # Rectangle(5, 5)
