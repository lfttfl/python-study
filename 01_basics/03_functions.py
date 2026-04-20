# Python 基础练习：函数
# =====================================================

# ── 一、函数定义与调用 ────────────────────────────────

# def 关键字用来定义函数，后面跟函数名和括号，括号内是参数列表
# 函数体必须缩进，表示属于这个函数
def greet():                          # 定义一个无参数的函数
    print("你好，欢迎学习 Python！")  # 函数体：调用时才执行

greet()                               # 调用函数：写函数名加括号即可执行

# 函数可以接收参数，让同一段代码处理不同的数据
def greet_user(name):                 # name 是参数，调用时传入实际值
    print(f"你好，{name}！")         # 用 f-string 把参数插入字符串

greet_user("小明")                    # 传入字符串 "小明" 作为 name 的值
greet_user("小红")                    # 同一函数，不同参数，得到不同结果

# ── 二、参数类型 ──────────────────────────────────────

print("\n── 位置参数 ──")

# 位置参数：调用时按顺序传入，顺序必须与定义时一致
def describe_pet(animal, name):       # 两个位置参数，顺序固定
    print(f"我有一只{animal}，叫{name}")

describe_pet("狗", "旺财")            # animal="狗"，name="旺财"
describe_pet("猫", "咪咪")            # animal="猫"，name="咪咪"

# 关键字传参：调用时写 参数名=值，顺序可以打乱
describe_pet(name="球球", animal="兔子")  # 顺序不同但结果正确

print("\n── 默认参数 ──")

# 默认参数：定义时给参数赋值，调用时可以省略该参数
# 默认参数必须放在位置参数的后面
def make_coffee(size, sugar=1, milk=False):   # sugar 默认 1，milk 默认 False
    print(f"制作{size}杯咖啡，糖{sugar}份，{'加' if milk else '不加'}牛奶")

make_coffee("大")                     # 只传 size，其余用默认值
make_coffee("中", sugar=2)            # 覆盖 sugar，milk 仍用默认值
make_coffee("小", sugar=0, milk=True) # 全部覆盖

print("\n── *args 可变位置参数 ──")

# *args：收集所有多余的位置参数，打包成一个 元组（tuple）
# 函数内部用 for 循环遍历即可处理任意数量的参数
def add_all(*args):                   # args 是元组，名字可随意，* 是关键
    print(f"接收到的参数：{args}")    # 打印元组，了解结构
    total = 0                         # 初始化累加器
    for num in args:                  # 遍历元组中每个数字
        total += num                  # 依次累加
    return total                      # 返回总和

print(add_all(1, 2, 3))               # 传 3 个数
print(add_all(10, 20, 30, 40, 50))    # 传 5 个数，函数定义不变

print("\n── **kwargs 可变关键字参数 ──")

# **kwargs：收集所有多余的关键字参数，打包成一个 字典（dict）
# 函数内部可像操作字典一样处理这些参数
def print_info(**kwargs):             # kwargs 是字典，** 是关键
    print(f"接收到的参数：{kwargs}")  # 打印字典，了解结构
    for key, value in kwargs.items(): # 遍历字典的键值对
        print(f"  {key}: {value}")    # 逐行打印每个字段

print_info(name="小明", age=18, city="北京")   # 三个关键字参数
print_info(brand="苹果", price=8999)           # 两个关键字参数

# 四种参数可以组合使用，顺序必须是：位置参数、默认参数、*args、**kwargs
def full_example(a, b=10, *args, **kwargs):
    print(f"a={a}, b={b}, args={args}, kwargs={kwargs}")

full_example(1)                          # a=1，其余全用默认/空
full_example(1, 2, 3, 4, x=5, y=6)      # 全部类型的参数都用上

# ── 三、返回值 ────────────────────────────────────────

print("\n── 返回值 ──")

# return 语句把结果传回给调用者；没有 return 则默认返回 None
def square(n):                        # 计算 n 的平方
    return n ** 2                     # ** 是幂运算，结果作为返回值

result = square(5)                    # 把返回值赋给变量
print(f"5 的平方是 {result}")         # 25

# 函数可以返回多个值，Python 自动打包成元组
def min_max(numbers):                 # 接收一个数字列表
    return min(numbers), max(numbers) # 逗号分隔，返回两个值

lo, hi = min_max([3, 1, 7, 2, 9])    # 解包元组，分别赋给 lo 和 hi
print(f"最小值={lo}，最大值={hi}")   # 1 和 9

# return 遇到条件时可以提前退出函数（卫语句）
def safe_divide(a, b):
    if b == 0:                        # 除数为 0 是非法操作
        return None                   # 提前返回 None，避免报错
    return a / b                      # 正常情况返回除法结果

print(safe_divide(10, 2))             # 5.0
print(safe_divide(10, 0))             # None

# ── 四、lambda 匿名函数 ───────────────────────────────

print("\n── lambda ──")

# lambda 参数: 表达式 —— 定义一个没有名字的小函数
# 只能写一个表达式，结果就是返回值，适合简单的一次性逻辑
double = lambda x: x * 2             # 相当于 def double(x): return x * 2
print(double(6))                      # 12

# lambda 常与 sorted()、map()、filter() 配合使用
students = [                          # 学生信息列表，每个元素是字典
    {"name": "小明", "score": 85},
    {"name": "小红", "score": 92},
    {"name": "小刚", "score": 78},
]

# sorted() 的 key 参数接收一个函数，决定按什么字段排序
by_score = sorted(students, key=lambda s: s["score"])   # 按分数升序
for s in by_score:
    print(f"  {s['name']}: {s['score']}")

# map(函数, 序列)：对序列每个元素调用函数，返回迭代器
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, nums))  # 每个数字平方
print(f"平方列表：{squares}")         # [1, 4, 9, 16, 25]

# filter(函数, 序列)：保留函数返回 True 的元素
evens = list(filter(lambda x: x % 2 == 0, nums))  # 只保留偶数
print(f"偶数列表：{evens}")           # [2, 4]

# ── 五、变量作用域 ────────────────────────────────────

print("\n── 变量作用域 ──")

# 全局变量：定义在函数外部，整个文件都能读取
global_var = "我是全局变量"           # 定义在模块顶层

def show_scope():
    local_var = "我是局部变量"        # 局部变量：只在函数内部存在
    print(global_var)                 # 函数内部可以读取全局变量
    print(local_var)                  # 局部变量在函数内部正常使用

show_scope()
# print(local_var)                    # 取消注释会报 NameError：函数外无法访问局部变量

# 如果要在函数内部修改全局变量，必须用 global 声明
counter = 0                           # 全局计数器

def increment():
    global counter                    # 声明要修改的是全局变量，而非创建局部变量
    counter += 1                      # 修改全局变量的值

increment()
increment()
print(f"counter = {counter}")         # 2，全局变量被修改了

# 局部变量与全局变量同名时，局部变量会"遮蔽"全局变量（shadowing）
value = "全局"                        # 全局 value

def shadow_demo():
    value = "局部"                    # 创建了一个新的局部变量，不影响全局
    print(f"函数内：{value}")         # 打印局部变量

shadow_demo()
print(f"函数外：{value}")             # 全局变量未被改变，仍是"全局"

# 嵌套函数与 nonlocal：修改外层（非全局）函数的变量
def outer():
    msg = "外层变量"                  # 外层函数的局部变量

    def inner():
        nonlocal msg                  # 声明要修改的是外层函数的 msg，而非创建新变量
        msg = "被内层修改了"          # 修改外层变量

    inner()                           # 调用内层函数
    print(msg)                        # 外层变量已被修改

outer()                               # 输出：被内层修改了

# ── 综合示例：成绩统计 ────────────────────────────────

print("\n── 综合示例：成绩统计 ──")

def analyze_scores(*scores, passing=60):  # *args 接收任意数量成绩，passing 是默认参数
    if not scores:                    # 如果没有传入任何成绩
        return None                   # 提前返回 None

    average = sum(scores) / len(scores)   # sum() 求和，len() 求个数
    highest = max(scores)             # 最高分
    lowest = min(scores)              # 最低分
    passed = list(filter(lambda s: s >= passing, scores))  # 筛选及格成绩

    return {                          # 返回字典，一次性返回多个统计结果
        "平均分": round(average, 1),  # round() 保留一位小数
        "最高分": highest,
        "最低分": lowest,
        "及格人数": len(passed),
        "及格率": f"{len(passed)/len(scores)*100:.1f}%",  # :.1f 保留一位小数
    }

report = analyze_scores(88, 72, 95, 54, 63, 41, 77, passing=60)
for key, val in report.items():       # 遍历字典，逐行打印统计结果
    print(f"  {key}: {val}")
