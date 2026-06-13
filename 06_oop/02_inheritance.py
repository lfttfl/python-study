# Python 面向对象编程：继承、多态、抽象基类
# =====================================================

from abc import ABC, abstractmethod           # ABC = Abstract Base Class

# ══════════════════════════════════════════════════════
# 一、单继承
# ══════════════════════════════════════════════════════

print("══ 一、单继承 ══")

# 子类通过 class 子类(父类) 语法继承父类的所有方法和属性
# 子类可以：① 直接继承（什么都不写）② 重写（覆盖父类方法）③ 扩展（调用 super() 后再追加）

class Animal:
    """所有动物的基类"""

    def __init__(self, name, weight):
        self.name   = name
        self.weight = weight

    def eat(self, food):
        return f"{self.name} 正在吃 {food}"

    def sleep(self):
        return f"{self.name} 正在睡觉"

    def speak(self):                            # 将被子类重写
        return f"{self.name} 发出了声音"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.weight}kg)"


class Dog(Animal):                             # Dog 继承 Animal
    """狗，继承自 Animal，扩展了 breed（品种）属性"""

    def __init__(self, name, weight, breed):
        super().__init__(name, weight)          # super() 调用父类 __init__，避免重复代码
        self.breed = breed                      # 子类自己的额外属性

    def speak(self):                            # 重写（override）：替换父类的实现
        return f"{self.name} 说：汪！"

    def fetch(self, item):                      # 新方法：Dog 特有，Animal 没有
        return f"{self.name} 捡回了 {item}"


class Cat(Animal):
    def __init__(self, name, weight, indoor=True):
        super().__init__(name, weight)
        self.indoor = indoor

    def speak(self):
        return f"{self.name} 说：喵～"

    def purr(self):
        return f"{self.name} 咕噜咕噜..."


dog = Dog("旺财", 15, "柴犬")
cat = Cat("咪咪", 4)

print(dog.speak())                              # 汪！（重写后的版本）
print(cat.speak())                              # 喵～
print(dog.eat("骨头"))                          # 继承自 Animal，直接可用
print(dog.fetch("飞盘"))                        # Dog 独有方法
print(repr(dog))                               # Dog('旺财', 15kg)

# isinstance：检查对象是否是某类（或其子类）的实例
print(f"\nisinstance(dog, Dog)：   {isinstance(dog, Dog)}")    # True
print(f"isinstance(dog, Animal)：{isinstance(dog, Animal)}") # True（Dog 是 Animal 的子类）
print(f"isinstance(cat, Dog)：   {isinstance(cat, Dog)}")     # False

# issubclass：检查类是否是某类的子类
print(f"issubclass(Dog, Animal)：{issubclass(Dog, Animal)}")  # True
print(f"issubclass(Cat, Dog)：  {issubclass(Cat, Dog)}")      # False

# __ class__ 和继承链
print(f"dog.__class__：{dog.__class__}")        # <class '__main__.Dog'>
print(f"Dog.__bases__：{Dog.__bases__}")        # (<class '__main__.Animal'>,)
print(f"Dog.__mro__：  {Dog.__mro__}")          # 方法解析顺序（MRO）

# ══════════════════════════════════════════════════════
# 二、super() 的正确用法
# ══════════════════════════════════════════════════════

print("\n══ 二、super() ══")

class Shape:
    def __init__(self, color="black"):
        self.color = color

    def describe(self):
        return f"颜色：{self.color}"


class Circle(Shape):
    def __init__(self, radius, color="black"):
        super().__init__(color)                 # 先初始化父类部分
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def describe(self):
        base = super().describe()               # 调用父类方法，获取父类的输出
        return f"{base}，圆形，半径={self.radius}"  # 在父类结果基础上扩展


class FilledCircle(Circle):                    # 三层继承：FilledCircle → Circle → Shape
    def __init__(self, radius, fill_color, border_color="black"):
        super().__init__(radius, border_color)  # 调用 Circle 的 __init__
        self.fill_color = fill_color

    def describe(self):
        base = super().describe()               # 调用 Circle 的 describe
        return f"{base}，填充色={self.fill_color}"

c  = Circle(5, "红")
fc = FilledCircle(3, "蓝", "黑")
print(c.describe())                             # 颜色：红，圆形，半径=5
print(fc.describe())                            # 颜色：黑，圆形，半径=3，填充色=蓝
print(f"FilledCircle MRO：{[cls.__name__ for cls in FilledCircle.__mro__]}")

# ══════════════════════════════════════════════════════
# 三、多态（Polymorphism）
# ══════════════════════════════════════════════════════

print("\n══ 三、多态 ══")

# 多态：不同类型的对象对同一消息（方法调用）有各自的响应
# Python 是鸭子类型：只要对象有对应的方法，就可以使用，无需显式声明接口

animals = [
    Dog("旺财", 15, "柴犬"),
    Cat("咪咪", 4),
    Animal("未知动物", 10),
]

print("── 多态调用 ──")
for animal in animals:
    print(f"  {animal.speak()}")               # 每个对象调用自己的 speak 实现

# make_sound 函数对所有动物通用，不需要知道具体类型
def make_sounds(animal_list):
    for a in animal_list:
        print(f"  [{type(a).__name__}] {a.speak()}")

make_sounds(animals)

# 鸭子类型：只要有 speak 方法，任何对象都能用
class Robot:
    def __init__(self, model):
        self.model = model
    def speak(self):
        return f"机器人 {self.model}：滴滴哒哒"

# Robot 不继承 Animal，但有 speak 方法，一样可以传入
mixed = animals + [Robot("R2D2")]
make_sounds(mixed)

# ══════════════════════════════════════════════════════
# 四、抽象基类（ABC）
# ══════════════════════════════════════════════════════

print("\n══ 四、抽象基类（ABC） ══")

# 抽象基类：定义接口规范，强制子类实现特定方法
# 抽象类不能直接实例化，用 @abstractmethod 标记必须实现的方法

class Shape2D(ABC):
    """所有二维图形的抽象基类"""

    def __init__(self, color="black"):
        self.color = color

    @abstractmethod
    def area(self) -> float:                   # 子类必须实现，否则无法实例化
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self):                        # 非抽象方法：子类直接继承，也可重写
        return (f"{self.__class__.__name__}  "
                f"面积={self.area():.2f}  周长={self.perimeter():.2f}")


class Rectangle(Shape2D):
    def __init__(self, w, h, color="black"):
        super().__init__(color)
        self.w, self.h = w, h

    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)


class Circle2D(Shape2D):
    import math as _math
    def __init__(self, r, color="black"):
        super().__init__(color)
        self.r = r

    def area(self):
        import math
        return math.pi * self.r ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.r


class Triangle(Shape2D):
    def __init__(self, a, b, c, color="black"):
        super().__init__(color)
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("不合法的三角形边长")
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = (self.a + self.b + self.c) / 2    # 海伦公式
        return (s * (s-self.a) * (s-self.b) * (s-self.c)) ** 0.5

    def perimeter(self): return self.a + self.b + self.c


# 抽象类不能直接实例化
try:
    s = Shape2D()
except TypeError as e:
    print(f"抽象类不能实例化：{e}")

shapes = [Rectangle(3, 4), Circle2D(5), Triangle(3, 4, 5)]
for s in shapes:
    print(f"  {s.describe()}")

# 抽象基类也可用于注册虚拟子类（不通过继承实现接口检查）
# 这里展示 isinstance 检查
print(f"Rectangle 是 Shape2D 的子类：{issubclass(Rectangle, Shape2D)}")

# ══════════════════════════════════════════════════════
# 五、多重继承与 Mixin
# ══════════════════════════════════════════════════════

print("\n══ 五、多重继承与 Mixin ══")

# Python 支持多重继承，方法解析顺序（MRO）由 C3 线性化算法决定
# Mixin：小型、专注单一功能的类，通过多重继承"混入"功能

class JSONMixin:
    """提供 JSON 序列化能力的 Mixin"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False, default=str)


class LogMixin:
    """提供操作日志的 Mixin"""
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")


class ValidateMixin:
    """提供通用验证能力的 Mixin"""
    def validate(self):
        # 子类可以重写 _validate_rules 来定义具体规则
        rules = getattr(self, "_validate_rules", [])
        errors = []
        for rule_fn, msg in rules:
            if not rule_fn(self):
                errors.append(msg)
        return errors


class User(JSONMixin, LogMixin, ValidateMixin):
    """用户类：通过 Mixin 获得 JSON 序列化、日志、验证能力"""

    def __init__(self, name, email, age):
        self.name  = name
        self.email = email
        self.age   = age
        self._validate_rules = [
            (lambda s: bool(s.name.strip()),        "用户名不能为空"),
            (lambda s: "@" in s.email,              "邮箱格式不正确"),
            (lambda s: 0 < s.age < 150,             "年龄不合法"),
        ]

    def __repr__(self):
        return f"User({self.name!r}, {self.email!r})"


u = User("小明", "xm@example.com", 18)
print(u.to_json())                              # {"name": "小明", "email": ...}
u.log("用户登录")                               # [User] 用户登录

errors = u.validate()
print(f"验证通过：{not errors}")                # True

bad_user = User("", "not-an-email", 999)
print(f"验证错误：{bad_user.validate()}")

# MRO 决定多重继承时方法的搜索顺序
print(f"\nUser MRO：{[c.__name__ for c in User.__mro__]}")
# User → JSONMixin → LogMixin → ValidateMixin → object

# ══════════════════════════════════════════════════════
# 六、综合示例：图形面积计算器
# ══════════════════════════════════════════════════════

print("\n══ 六、综合示例 ══")

class ShapeRegistry:
    """形状注册表：用类变量维护所有已注册的形状类"""
    _registry = {}

    @classmethod
    def register(cls, name):
        def decorator(shape_cls):
            cls._registry[name] = shape_cls
            return shape_cls
        return decorator

    @classmethod
    def create(cls, name, *args, **kwargs):
        if name not in cls._registry:
            raise ValueError(f"未知形状：{name}")
        return cls._registry[name](*args, **kwargs)

    @classmethod
    def total_area(cls, shapes):
        return sum(s.area() for s in shapes)


@ShapeRegistry.register("矩形")
class Rect(Shape2D):
    def __init__(self, w, h):
        super().__init__()
        self.w, self.h = w, h
    def area(self):      return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)


@ShapeRegistry.register("圆形")
class Circ(Shape2D):
    def __init__(self, r):
        import math
        super().__init__()
        self.r = r
    def area(self):
        import math
        return math.pi * self.r ** 2
    def perimeter(self):
        import math
        return 2 * math.pi * self.r


shapes = [
    ShapeRegistry.create("矩形", 3, 4),
    ShapeRegistry.create("圆形", 5),
    ShapeRegistry.create("矩形", 6, 2),
]

for s in shapes:
    print(f"  {s.describe()}")

print(f"总面积：{ShapeRegistry.total_area(shapes):.2f}")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("\n══ 练习题 ══")
print("""
1. 定义抽象基类 Vehicle（交通工具），包含抽象方法 fuel_type() 和 max_speed()，
   以及具体方法 describe()。实现子类 Car（汽车）、Bicycle（自行车）、Boat（船）。

2. 创建 SerializeMixin，提供 to_dict() 方法（返回实例 __dict__ 的副本，
   去除以 _ 开头的私有字段）。让 Car 同时继承 Vehicle 和 SerializeMixin。

3. 实现一个简单的"员工层级"：
   - Employee（基类）：name、salary
   - Manager（继承 Employee）：额外有 team_size，工资加 20% 奖金
   - Director（继承 Manager）：额外有 budget，工资再加 30% 奖金
   用多态实现 pay_report(employees) 函数，打印每人实际工资。

参考答案见下方注释：
""")

# # 答案3：
# class Employee:
#     def __init__(self, name, salary):
#         self.name, self.salary = name, salary
#     def actual_salary(self):  return self.salary
#     def __repr__(self):       return f"{self.__class__.__name__}({self.name})"
#
# class Manager(Employee):
#     def __init__(self, name, salary, team_size):
#         super().__init__(name, salary)
#         self.team_size = team_size
#     def actual_salary(self): return self.salary * 1.2
#
# class Director(Manager):
#     def __init__(self, name, salary, team_size, budget):
#         super().__init__(name, salary, team_size)
#         self.budget = budget
#     def actual_salary(self): return self.salary * 1.2 * 1.3
#
# def pay_report(employees):
#     for e in employees:
#         print(f"  {e.name}（{type(e).__name__}）：¥{e.actual_salary():,.2f}")
#
# pay_report([Employee("Alice", 10000), Manager("Bob", 12000, 5), Director("Carol", 15000, 10, 1e6)])
