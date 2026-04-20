# Python 函数进阶练习：闭包、装饰器、递归、高阶函数
# =====================================================

import time                                   # 用于计时，演示装饰器实际应用
import functools                              # 提供 wraps、reduce 等工具

# ══════════════════════════════════════════════════════
# 一、闭包（Closure）
# ══════════════════════════════════════════════════════

# 闭包的三个条件：
#   1. 有一个外层函数（enclosing function）
#   2. 外层函数内定义了内层函数
#   3. 内层函数引用了外层函数的局部变量（自由变量）
# 当外层函数执行完毕后，其局部变量并不销毁，
# 而是被内层函数"捕获"，随内层函数对象一起存活

print("══ 一、闭包 ══")

# ── 1-1 最简单的闭包 ──────────────────────────────────

def make_greeting(prefix):                    # 外层函数，接受一个"配置"参数
    """返回一个绑定了 prefix 的问候函数"""
    def greet(name):                          # 内层函数，引用了外层的 prefix
        return f"{prefix}，{name}！"          # prefix 是自由变量（free variable）
    return greet                              # 返回内层函数对象本身，不是调用结果

hello  = make_greeting("你好")               # hello 是一个闭包对象，prefix="你好" 被捕获
hi     = make_greeting("Hi")                 # hi 是另一个闭包，prefix="Hi" 独立存储

print(hello("小明"))                          # 你好，小明！
print(hi("Alice"))                            # Hi，Alice！
print(hello("小红"))                          # 你好，小红！（两个闭包互不干扰）

# 查看闭包捕获的自由变量
print("捕获的变量名：", greet.__code__.co_freevars if False else hello.__code__.co_freevars)
print("捕获的变量值：", hello.__closure__[0].cell_contents)   # "你好"

# ── 1-2 闭包维持状态（替代简单的类）────────────────

print("\n── 闭包维持状态 ──")

def make_counter(start=0, step=1):            # 外层函数：配置计数器的初始值和步长
    count = [start]                           # 用列表包裹整数，使内层函数可以修改它
                                              # （也可以用 nonlocal，见下方示例）
    def counter():                            # 内层函数：每次调用都累加
        count[0] += step                      # 修改列表元素（不需要 nonlocal）
        return count[0]                       # 返回当前计数值
    return counter

c1 = make_counter()                           # 默认从 0 开始，步长 1
c2 = make_counter(start=10, step=5)          # 从 10 开始，步长 5

print(c1(), c1(), c1())                       # 1 2 3（每次调用自增）
print(c2(), c2(), c2())                       # 15 20 25（独立状态，互不影响）

# 用 nonlocal 的写法（更 Pythonic，变量不需要包装成列表）
def make_counter_v2(start=0):
    count = start                             # 普通整数，外层局部变量
    def counter():
        nonlocal count                        # 声明 count 是外层变量，允许修改
        count += 1                            # 直接修改整数（nonlocal 让赋值不创建新局部变量）
        return count
    return counter

c3 = make_counter_v2()
print(c3(), c3(), c3())                       # 1 2 3

# ── 1-3 闭包工厂：批量生成函数 ────────────────────────

print("\n── 闭包工厂 ──")

def make_power(exp):                          # 工厂函数：生成"求 exp 次方"的函数
    def power(base):                          # 内层函数捕获 exp
        return base ** exp
    power.__name__ = f"power_{exp}"          # 动态设置函数名，方便调试
    return power

square = make_power(2)                        # 平方函数
cube   = make_power(3)                        # 立方函数
pow5   = make_power(5)                        # 五次方函数

print(f"3² = {square(3)}")                    # 9
print(f"3³ = {cube(3)}")                      # 27
print(f"2⁵ = {pow5(2)}")                      # 32

# 用列表推导式批量创建——经典陷阱演示
# 错误写法：所有函数共享同一个循环变量 i
wrong_funcs = [lambda x: x * i for i in range(5)]   # i 是循环变量，循环结束后 i=4
print("陷阱写法结果：", [f(2) for f in wrong_funcs])  # [8, 8, 8, 8, 8]，全是 2*4

# 正确写法：用默认参数把当前 i 的值"固化"到函数内部
correct_funcs = [lambda x, n=i: x * n for i in range(5)]  # n=i 在定义时求值
print("正确写法结果：", [f(2) for f in correct_funcs])     # [0, 2, 4, 6, 8]

# ── 1-4 闭包实现记忆化（手动版 lru_cache）─────────────

print("\n── 闭包实现记忆化 ──")

def memoize(func):                            # 接受一个函数，返回带缓存功能的新函数
    cache = {}                                # 缓存字典，键是参数，值是计算结果
    def wrapper(*args):                       # 包装函数，捕获 cache 和 func
        if args not in cache:                 # 首次调用才真正计算
            cache[args] = func(*args)         # 把结果存入缓存
        return cache[args]                    # 命中缓存直接返回
    wrapper.cache = cache                     # 把缓存暴露出来，方便外部查看
    return wrapper

@memoize                                      # 等价于 slow_fib = memoize(slow_fib)
def slow_fib(n):                              # 原本是指数时间复杂度的朴素递归
    if n <= 1:
        return n
    return slow_fib(n - 1) + slow_fib(n - 2)

print(slow_fib(35))                           # 9227465，加了缓存后瞬间完成
print("缓存大小：", len(slow_fib.cache))       # 36（0 到 35 各缓存一次）

# ══════════════════════════════════════════════════════
# 二、装饰器（Decorator）
# ══════════════════════════════════════════════════════

print("\n══ 二、装饰器 ══")

# 装饰器本质是一个接受函数并返回函数的高阶函数
# @ 语法糖让代码更简洁：
#   @decorator
#   def func(): ...
# 等价于：func = decorator(func)

# ── 2-1 基础装饰器 ────────────────────────────────────

print("\n── 基础装饰器 ──")

def timer(func):                              # 装饰器函数，接受被装饰的函数
    @functools.wraps(func)                    # 保留原函数的 __name__、__doc__ 等元信息
    def wrapper(*args, **kwargs):             # wrapper 接受任意参数，原封不动传给 func
        start = time.perf_counter()           # 高精度计时开始（perf_counter 比 time 精确）
        result = func(*args, **kwargs)        # 调用原函数，保存返回值
        elapsed = time.perf_counter() - start # 计算耗时
        print(f"[timer] {func.__name__} 耗时 {elapsed:.6f} 秒")
        return result                         # 必须返回原函数的结果，否则调用方拿不到值
    return wrapper                            # 返回包装后的函数

@timer                                        # 给 slow_sum 套上计时器
def slow_sum(n):
    """计算 1 到 n 的总和（故意用循环让耗时可见）"""
    total = 0
    for i in range(n + 1):
        total += i
    return total

result = slow_sum(1_000_000)                  # 下划线是数字分隔符，等于 1000000
print(f"slow_sum(1_000_000) = {result:,}")   # 500000500000

# functools.wraps 的效果：函数名和文档字符串被正确保留
print(f"函数名：{slow_sum.__name__}")         # slow_sum（没有 wraps 会显示 wrapper）
print(f"文档：{slow_sum.__doc__}")            # 计算 1 到 n 的总和（故意用循环让耗时可见）

# ── 2-2 装饰器叠加（多个装饰器）──────────────────────

print("\n── 装饰器叠加 ──")

def logger(func):                             # 记录调用信息的装饰器
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[logger] 调用 {func.__name__}，参数 args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[logger] {func.__name__} 返回：{result}")
        return result
    return wrapper

# 多个装饰器叠加：从下到上依次包装，从外到内依次执行
# @logger @timer def add(...) 等价于 add = logger(timer(add))
# 调用顺序：logger.wrapper → timer.wrapper → add 原函数 → timer.wrapper → logger.wrapper
@logger
@timer
def add(a, b):
    return a + b

add(3, 5)                                     # 先打印 logger 进入，再打印 timer 耗时，再打印 logger 返回

# ── 2-3 带参数的装饰器 ────────────────────────────────

print("\n── 带参数的装饰器 ──")

# 带参数的装饰器需要三层嵌套：
#   最外层接收装饰器的参数（配置层）
#   中间层接收被装饰的函数
#   最内层是实际的包装函数
def retry(max_times=3, delay=0.0):            # 第一层：接收装饰器参数
    def decorator(func):                      # 第二层：接收被装饰的函数
        @functools.wraps(func)
        def wrapper(*args, **kwargs):         # 第三层：实际包装逻辑
            for attempt in range(1, max_times + 1):   # 最多重试 max_times 次
                try:
                    return func(*args, **kwargs)       # 成功则直接返回
                except Exception as e:
                    print(f"  第{attempt}次失败：{e}")
                    if attempt < max_times:            # 还有重试机会
                        if delay > 0:
                            time.sleep(delay)          # 等待后再试
                    else:
                        raise                          # 全部失败则向上抛出异常
        return wrapper
    return decorator                          # 第一层返回真正的装饰器

# 模拟一个偶尔失败的函数（前两次抛异常，第三次成功）
_call_count = {"n": 0}                        # 用字典避免 nonlocal 的限制

@retry(max_times=3, delay=0.0)               # 带参数：最多重试 3 次，不等待
def unstable_api():
    _call_count["n"] += 1
    if _call_count["n"] < 3:                 # 前两次故意失败
        raise ConnectionError("网络超时")
    return "成功响应"

print(unstable_api())                         # 前两次失败后第三次成功

# ── 2-4 类装饰器 ──────────────────────────────────────

print("\n── 类装饰器 ──")

# 类也可以作为装饰器：实现 __init__ 接收函数，__call__ 实现包装逻辑
class CallCounter:                            # 统计函数被调用次数的装饰器
    def __init__(self, func):                 # 初始化时接收被装饰的函数
        functools.update_wrapper(self, func)  # 等同于 wraps，更新类的元信息
        self.func   = func                    # 保存原函数
        self.count  = 0                       # 初始化调用计数器

    def __call__(self, *args, **kwargs):      # 每次"调用"装饰后的函数时触发
        self.count += 1                       # 计数加一
        print(f"[CallCounter] {self.func.__name__} 第 {self.count} 次调用")
        return self.func(*args, **kwargs)     # 调用原函数并返回结果

@CallCounter                                  # greet 变成了 CallCounter 的实例
def greet(name):
    return f"你好，{name}！"

print(greet("小明"))                          # 第 1 次
print(greet("小红"))                          # 第 2 次
print(greet("小刚"))                          # 第 3 次
print(f"总共调用了 {greet.count} 次")         # 3

# ── 2-5 实用装饰器：缓存、权限控制 ───────────────────

print("\n── 实用装饰器 ──")

# functools.lru_cache：Python 内置的 LRU 缓存装饰器（比手写 memoize 更强）
@functools.lru_cache(maxsize=128)             # maxsize 是缓存上限，None 表示无限
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(fib_cached(40))                         # 102334155，瞬间完成
print(fib_cached.cache_info())                # 命中次数、未命中次数、缓存大小

# 权限控制装饰器（模拟登录验证）
def require_login(func):
    @functools.wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.get("logged_in"):         # 检查用户是否已登录
            raise PermissionError(f"用户 {user['name']} 未登录，拒绝访问")
        return func(user, *args, **kwargs)    # 通过验证才执行原函数
    return wrapper

@require_login
def view_profile(user):
    return f"欢迎，{user['name']}！您的积分：{user.get('points', 0)}"

logged_in_user  = {"name": "小明", "logged_in": True,  "points": 520}
anonymous_user  = {"name": "游客", "logged_in": False}

print(view_profile(logged_in_user))           # 正常显示
try:
    view_profile(anonymous_user)              # 触发权限检查
except PermissionError as e:
    print(f"权限拒绝：{e}")

# ══════════════════════════════════════════════════════
# 三、递归函数
# ══════════════════════════════════════════════════════

print("\n══ 三、递归函数 ══")

# 递归的两个必要条件：
#   1. 基准情况（base case）：不再递归，直接返回结果，防止无限循环
#   2. 递推关系（recursive case）：把问题分解为规模更小的同类子问题

# ── 3-1 阶乘 ──────────────────────────────────────────

print("\n── 阶乘 ──")

def factorial_recursive(n):                   # 递归版本
    if n < 0:                                 # 输入校验：负数没有阶乘
        raise ValueError("n 必须是非负整数")
    if n == 0 or n == 1:                      # 基准情况：0! = 1! = 1
        return 1
    return n * factorial_recursive(n - 1)     # 递推：n! = n × (n-1)!

def factorial_iterative(n):                   # 迭代版本（for 循环）
    if n < 0:
        raise ValueError("n 必须是非负整数")
    result = 1                                # 累乘器初始化为 1
    for i in range(2, n + 1):               # 从 2 乘到 n（0 和 1 不影响结果）
        result *= i
    return result

for n in [0, 1, 5, 10]:
    r = factorial_recursive(n)
    i = factorial_iterative(n)
    print(f"  {n}! = {r}（递归）= {i}（迭代）匹配：{r == i}")

# ── 3-2 斐波那契数列 ───────────────────────────────────

print("\n── 斐波那契 ──")

def fib_naive(n):                             # 朴素递归：直观但指数级时间复杂度 O(2^n)
    if n <= 1:                                # 基准：F(0)=0, F(1)=1
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)   # 大量重复计算！

def fib_memo(n, memo={}):                    # 记忆化递归：用字典缓存，降至 O(n)
    if n in memo:                             # 已算过直接取缓存
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)  # 存入缓存
    return memo[n]

def fib_iterative(n):                        # 迭代版本：O(n) 时间，O(1) 空间，最优
    if n <= 1:
        return n
    prev, curr = 0, 1                         # 只保留相邻两个值，节省内存
    for _ in range(2, n + 1):               # 从第 2 项开始滚动计算
        prev, curr = curr, prev + curr        # 同时更新两个变量（Python 元组赋值）
    return curr

for n in [0, 1, 5, 10, 20]:
    print(f"  F({n:2d}) = {fib_iterative(n):6d}  memo={fib_memo(n)}")

# 性能对比：朴素递归 vs 记忆化递归 vs 迭代
print("\n性能对比（n=30）：")
t0 = time.perf_counter()
fib_naive(30)
print(f"  朴素递归：{time.perf_counter() - t0:.4f} 秒")  # 约 0.2~0.5 秒

t0 = time.perf_counter()
fib_memo(30)
print(f"  记忆化：  {time.perf_counter() - t0:.6f} 秒")  # 微秒级

t0 = time.perf_counter()
fib_iterative(30)
print(f"  迭代：    {time.perf_counter() - t0:.6f} 秒")  # 微秒级

# ── 3-3 其他递归经典：汉诺塔 ─────────────────────────

print("\n── 汉诺塔 ──")

def hanoi(n, src, dst, via):                  # n 块圆盘，从 src 柱经由 via 移到 dst 柱
    if n == 1:                                # 基准：只有一块，直接移动
        print(f"  移动圆盘 1：{src} → {dst}")
        return
    hanoi(n - 1, src, via, dst)              # 第一步：把上面 n-1 块移到 via 柱
    print(f"  移动圆盘 {n}：{src} → {dst}")  # 第二步：把最大的圆盘移到 dst
    hanoi(n - 1, via, dst, src)              # 第三步：把 n-1 块从 via 移到 dst

hanoi(3, "A", "C", "B")                      # 3 块圆盘，需要 2^3-1=7 步
print(f"  （n 块汉诺塔需要 2^n - 1 步）")

# ── 3-4 递归 vs 迭代的选择原则 ────────────────────────

print("\n── 递归 vs 迭代 ──")

# Python 默认递归深度限制是 1000（sys.getrecursionlimit()）
import sys
print(f"默认递归深度上限：{sys.getrecursionlimit()}")   # 1000

# 二叉树遍历天然适合递归（迭代反而复杂），数值计算适合迭代
# 原则：问题本身具有递归结构时用递归，否则优先用迭代

# 用迭代实现"展开嵌套列表"（递归写法更直观）
def flatten_recursive(nested):               # 递归版本：遇到列表就递归展开
    result = []
    for item in nested:
        if isinstance(item, list):            # isinstance 判断类型
            result.extend(flatten_recursive(item))  # 递归处理子列表
        else:
            result.append(item)              # 非列表直接追加
    return result

nested = [1, [2, [3, 4], 5], [6, 7], 8]
print("展开嵌套列表：", flatten_recursive(nested))   # [1, 2, 3, 4, 5, 6, 7, 8]

# ══════════════════════════════════════════════════════
# 四、高阶函数（Higher-Order Functions）
# ══════════════════════════════════════════════════════

print("\n══ 四、高阶函数 ══")

# 高阶函数：接受函数作为参数 或 返回函数作为结果（或两者都有）
# Python 中函数是"一等公民"（first-class citizen）：
#   可以赋值给变量、存入列表、作为参数传递、作为返回值

# ── 4-1 函数作为参数 ──────────────────────────────────

print("\n── 函数作为参数 ──")

def apply_twice(func, value):                 # 接受函数 func 和初始值 value
    """把 func 对 value 应用两次"""
    return func(func(value))                  # 第一次：func(value)；第二次：func(func(value))

double = lambda x: x * 2                     # 定义一个翻倍函数
add10  = lambda x: x + 10                    # 定义一个加 10 的函数

print(apply_twice(double, 3))                 # double(double(3)) = double(6) = 12
print(apply_twice(add10, 5))                  # add10(add10(5)) = add10(15) = 25

# 自定义 map：把函数应用到列表每个元素
def my_map(func, iterable):
    return [func(item) for item in iterable]  # 列表推导式实现

# 自定义 filter：保留满足条件的元素
def my_filter(predicate, iterable):           # predicate 是"谓词函数"，返回布尔值
    return [item for item in iterable if predicate(item)]

# 自定义 reduce：把列表归约为单个值
def my_reduce(func, iterable, initial=None):
    it = iter(iterable)                       # 把可迭代对象转为迭代器
    acc = initial if initial is not None else next(it)  # 初始累积值
    for item in it:                           # 逐个取出元素
        acc = func(acc, item)                 # 把累积值和当前元素合并
    return acc

nums = [1, 2, 3, 4, 5]
print("my_map 平方：",    my_map(lambda x: x**2, nums))         # [1, 4, 9, 16, 25]
print("my_filter 偶数：", my_filter(lambda x: x%2==0, nums))    # [2, 4]
print("my_reduce 乘积：", my_reduce(lambda a, b: a*b, nums))    # 120

# functools.reduce（标准库版本）
from functools import reduce
print("reduce 乘积：", reduce(lambda a, b: a * b, nums))        # 120
print("reduce 最大：", reduce(lambda a, b: a if a > b else b, nums))  # 5

# ── 4-2 函数作为返回值 ────────────────────────────────

print("\n── 函数作为返回值 ──")

def make_validator(*rules):                   # 接受若干验证规则函数
    """组合多个规则，返回一个综合验证函数"""
    def validate(value):                      # 综合验证函数
        errors = []
        for rule in rules:                    # 依次应用每条规则
            ok, msg = rule(value)             # 每条规则返回 (是否通过, 错误信息)
            if not ok:
                errors.append(msg)            # 收集失败原因
        return len(errors) == 0, errors       # 全部通过则合法
    return validate

# 定义几条验证规则（每条都是函数，接受值，返回 (bool, str)）
def rule_not_empty(v):
    return (bool(v.strip()), "不能为空")

def rule_min_len(n):                          # 工厂函数：生成"最小长度"规则
    return lambda v: (len(v) >= n, f"长度不能少于 {n} 个字符")

def rule_no_space(v):
    return (" " not in v, "不能包含空格")

# 组合规则，生成密码验证函数
validate_password = make_validator(
    rule_not_empty,
    rule_min_len(8),
    rule_no_space,
)

for pwd in ["", "abc", "abc defgh", "strongpwd"]:
    ok, errors = validate_password(pwd)
    status = "✓" if ok else "✗"
    print(f"  [{status}] '{pwd}' → {errors if errors else '合法'}")

# ── 4-3 函数组合与管道 ────────────────────────────────

print("\n── 函数组合 ──")

def compose(*funcs):                          # 接受任意多个函数，返回它们的组合
    """f∘g∘h(x) = f(g(h(x)))，从右往左依次应用"""
    def composed(x):
        result = x
        for func in reversed(funcs):          # reversed：从最右边的函数开始
            result = func(result)
        return result
    return composed

def pipe(*funcs):                             # 与 compose 相反：从左往右依次应用（管道风格）
    """pipe(f, g, h)(x) = h(g(f(x)))"""
    def piped(x):
        result = x
        for func in funcs:                    # 从第一个函数开始
            result = func(result)
        return result
    return piped

strip   = str.strip                           # 去除首尾空白（使用内置字符串方法）
to_upper = str.upper                          # 转大写
add_bang = lambda s: s + "!"                  # 加感叹号

# compose：从右到左，先 strip，再 upper，再加 !
process1 = compose(add_bang, to_upper, strip)
print(process1("  hello world  "))            # HELLO WORLD!

# pipe：从左到右，先 strip，再 upper，再加 !
process2 = pipe(strip, to_upper, add_bang)
print(process2("  hello world  "))            # HELLO WORLD!（结果相同，写法更直观）

# ── 4-4 偏函数（partial）────────────────────────────

print("\n── 偏函数 ──")

# functools.partial：固定函数的部分参数，生成新函数（特化版本）
# 避免重复传入固定参数，提高代码复用性
from functools import partial

def power(base, exp):                         # 普通函数：两个参数
    return base ** exp

square2 = partial(power, exp=2)              # 固定 exp=2，生成"平方"函数
cube2   = partial(power, exp=3)              # 固定 exp=3，生成"立方"函数

print(square2(5))                             # 25（只需传 base）
print(cube2(4))                               # 64

# partial 常用于配合 map/filter 简化 lambda
from functools import partial
int_base2 = partial(int, base=2)             # 固定 base=2，生成"二进制字符串转整数"函数
binary_strings = ["1010", "1111", "0101"]
print(list(map(int_base2, binary_strings)))   # [10, 15, 5]

# ── 4-5 综合示例：数据处理管道 ───────────────────────

print("\n── 综合示例：数据处理管道 ──")

# 原始数据：学生成绩（含脏数据）
raw_data = [
    {"name": "  小明 ", "score": "88"},       # 姓名有空格，分数是字符串
    {"name": "小红",    "score": "95"},
    {"name": "小刚",    "score": "invalid"},  # 无效分数
    {"name": "",        "score": "72"},       # 空姓名
    {"name": "小李",    "score": "45"},       # 不及格
    {"name": "小王",    "score": "78"},
]

# 用高阶函数构建处理管道，每一步都是纯函数（不修改原数据）

def clean_name(record):                       # 步骤1：清理姓名空白
    return {**record, "name": record["name"].strip()}   # ** 展开字典，只覆盖 name

def parse_score(record):                      # 步骤2：分数字符串转整数，失败返回 None
    try:
        return {**record, "score": int(record["score"])}
    except ValueError:
        return {**record, "score": None}      # 无效分数标记为 None

def is_valid(record):                         # 过滤器：姓名非空且分数有效
    return bool(record["name"]) and record["score"] is not None

def is_passing(record):                       # 过滤器：及格（60分以上）
    return record["score"] >= 60

def add_grade(record):                        # 步骤3：根据分数添加等级字段
    score = record["score"]
    grade = "优秀" if score >= 90 else "良好" if score >= 75 else "及格"
    return {**record, "grade": grade}

# 管道执行：map（清洗）→ map（解析）→ filter（过滤无效）→ filter（过滤不及格）→ map（打标签）
pipeline = pipe(
    lambda data: map(clean_name, data),       # 清理空白
    lambda data: map(parse_score, data),      # 解析分数
    lambda data: filter(is_valid, data),      # 过滤无效记录
    lambda data: filter(is_passing, data),    # 过滤不及格
    lambda data: map(add_grade, data),        # 添加等级
    list,                                     # 最终转换为列表（消费所有惰性迭代器）
)

results = pipeline(raw_data)

print(f"{'姓名':<6}{'分数':>6}{'等级':>6}")
print("-" * 20)
for r in sorted(results, key=lambda x: x["score"], reverse=True):
    print(f"{r['name']:<6}{r['score']:>6}{r['grade']:>6}")
