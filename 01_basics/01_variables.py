# Python 基础练习：变量类型、字符串操作、类型转换
# =====================================================

# ── 一、变量类型 ──────────────────────────────────────

name = "小明"          # str（字符串）：用引号包裹的文字
age = 18               # int（整数）：没有小数点的数字
height = 1.75          # float（浮点数）：带小数点的数字
is_student = True      # bool（布尔值）：只有 True 或 False 两种值
nothing = None         # NoneType：表示"没有值"或"空"

# type() 函数可以查看变量的类型
print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>
print(type(height))    # <class 'float'>
print(type(is_student))# <class 'bool'>
print(type(nothing))   # <class 'NoneType'>

# ── 二、字符串操作 ────────────────────────────────────

greeting = "Hello, World!"   # 定义一个字符串变量

# len() 返回字符串的字符数（包括空格和标点）
print(len(greeting))         # 13

# 索引：字符串每个字符都有编号，从 0 开始，-1 表示最后一个
print(greeting[0])           # H  （第 1 个字符）
print(greeting[-1])          # !  （最后一个字符）

# 切片：[起始:结束] 取出一段子字符串，不包含结束位置
print(greeting[0:5])         # Hello

# upper() / lower() 转大小写，原字符串不变，返回新字符串
print(greeting.upper())      # HELLO, WORLD!
print(greeting.lower())      # hello, world!

# strip() 去掉字符串两端的空白（空格、换行等）
messy = "  你好  "
print(messy.strip())         # 你好

# replace(旧, 新) 把字符串中所有"旧"替换成"新"
print(greeting.replace("World", "Python"))  # Hello, Python!

# split(分隔符) 按分隔符把字符串拆成列表
words = "苹果,香蕉,橙子"
print(words.split(","))      # ['苹果', '香蕉', '橙子']

# in 关键字：检查子字符串是否存在
print("Hello" in greeting)   # True
print("Python" in greeting)  # False

# f-string（格式化字符串）：花括号 {} 内直接写变量或表达式
intro = f"我叫{name}，今年{age}岁，身高{height}米"
print(intro)                  # 我叫小明，今年18岁，身高1.75米

# ── 三、类型转换 ──────────────────────────────────────

# int() 把字符串或浮点数转换成整数（小数部分直接截断，不四舍五入）
print(int("42"))              # 42
print(int(3.99))              # 3   ← 注意：截断不是四舍五入

# float() 把字符串或整数转换成浮点数
print(float("3.14"))          # 3.14
print(float(10))              # 10.0

# str() 把数字转换成字符串（数字不能直接和字符串用 + 拼接，需先转换）
score = 95
print("我的分数是：" + str(score))   # 我的分数是：95

# bool() 判断一个值的"真假"：0、空字符串、None、空列表都是 False
print(bool(0))                # False
print(bool(""))               # False
print(bool(None))             # False
print(bool(42))               # True
print(bool("hello"))          # True

# 用户输入 input() 返回的永远是字符串，需要手动转换类型
# user_age = int(input("请输入你的年龄："))   # 取消注释可交互运行

# ── 综合示例 ─────────────────────────────────────────

print("\n── 综合示例 ──")
radius = 5                         # 圆的半径（整数）
pi = 3.14159                       # 圆周率（浮点数）
area = pi * radius ** 2            # ** 是幂运算，radius**2 = 25
print(f"半径为 {radius} 的圆，面积 = {area:.2f}")  # :.2f 保留两位小数
