# Python 基础练习：推导式与常用内置函数
# =====================================================

# ── 一、列表推导式 ─────────────────────────────────────

# 列表推导式语法：[表达式 for 变量 in 可迭代对象 (if 条件)]
# 作用：用一行代码生成列表，比 for 循环更简洁

# 传统写法：用 for 循环生成平方列表
squares_loop = []                         # 先建空列表
for n in range(1, 6):                     # 遍历 1 到 5
    squares_loop.append(n ** 2)           # 把平方值追加进去
print("for 循环：", squares_loop)         # [1, 4, 9, 16, 25]

# 推导式写法：等价于上面的 for 循环，一行搞定
squares = [n ** 2 for n in range(1, 6)]  # n**2 是表达式，range(1,6) 是数据源
print("列表推导式：", squares)            # [1, 4, 9, 16, 25]

# 带 if 过滤：只保留满足条件的元素
evens = [n for n in range(10) if n % 2 == 0]  # 只取偶数（余数为 0）
print("偶数列表：", evens)                # [0, 2, 4, 6, 8]

# 表达式里可以做任意运算，不限于简单值
words = ["hello", "world", "python"]     # 原始单词列表
upper_words = [w.upper() for w in words] # 每个单词调用 upper() 转大写
print("大写列表：", upper_words)          # ['HELLO', 'WORLD', 'PYTHON']

# 嵌套推导式：外层 for 控制行，内层 for 控制列，展开二维结构
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]         # 3×3 矩阵（列表的列表）
flat = [elem for row in matrix for elem in row]      # 先遍历行，再遍历行内元素
print("展开矩阵：", flat)                 # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# if-else 放在表达式位置（三元）：对每个元素做不同处理
labels = ["偶数" if n % 2 == 0 else "奇数" for n in range(6)]
print("奇偶标签：", labels)              # ['偶数', '奇数', '偶数', '奇数', '偶数', '奇数']

# ── 二、字典推导式 ─────────────────────────────────────

print("\n── 字典推导式 ──")

# 字典推导式语法：{键表达式: 值表达式 for 变量 in 可迭代对象 (if 条件)}
students = ["小明", "小红", "小刚"]      # 学生姓名列表
scores = [88, 92, 75]                    # 对应分数列表

# zip() 把两个列表"拉链式"配对，生成 (名字, 分数) 的元组序列
score_dict = {name: score for name, score in zip(students, scores)}
print("成绩字典：", score_dict)          # {'小明': 88, '小红': 92, '小刚': 75}

# 带条件：只保留分数 >= 80 的学生
top_dict = {name: score for name, score in score_dict.items() if score >= 80}
print("优秀学生：", top_dict)            # {'小明': 88, '小红': 92}

# 对值做变换：把分数统一加 5（模拟加分）
boosted = {name: score + 5 for name, score in score_dict.items()}
print("加分后：", boosted)               # {'小明': 93, '小红': 97, '小刚': 80}

# 反转字典：把键和值互换（前提是值唯一）
inverted = {v: k for k, v in score_dict.items()}   # 分数作键，姓名作值
print("反转字典：", inverted)            # {88: '小明', 92: '小红', 75: '小刚'}

# ── 三、集合推导式 ─────────────────────────────────────

print("\n── 集合推导式 ──")

# 集合推导式语法：{表达式 for 变量 in 可迭代对象}
# 集合自动去重，结果是无序的（打印顺序不固定）
nums_with_dup = [1, 2, 2, 3, 3, 3, 4]   # 含重复元素的列表
unique_squares = {n ** 2 for n in nums_with_dup}  # 平方后自动去掉重复值
print("去重平方集合：", unique_squares)  # {1, 4, 9, 16}（顺序可能不同）

# 利用集合推导式快速提取唯一值
sentences = ["我 爱 Python", "Python 很 好用", "我 喜欢 编程"]
all_words = {w for sentence in sentences for w in sentence.split()}  # 拆词后去重
print("不重复的词：", all_words)         # 顺序不定，但每个词只出现一次

# ── 四、map() ──────────────────────────────────────────

print("\n── map() ──")

# map(函数, 可迭代对象)：对每个元素应用函数，返回惰性迭代器（不立即计算）
# 需要用 list() 转换才能看到所有结果
prices = [29.9, 49.5, 15.0, 99.8]        # 原价列表

# 用 lambda 定义打折逻辑，map 批量应用
discounted = list(map(lambda p: round(p * 0.8, 1), prices))  # 八折
print("打折后：", discounted)             # [23.9, 39.6, 12.0, 79.8]

# map 也可以接收普通函数
def celsius_to_fahrenheit(c):            # 摄氏转华氏公式
    return c * 9 / 5 + 32               # 标准换算公式

temps_c = [0, 20, 37, 100]              # 摄氏温度列表
temps_f = list(map(celsius_to_fahrenheit, temps_c))  # 批量转换
print("华氏温度：", temps_f)             # [32.0, 68.0, 98.6, 212.0]

# map 支持多个序列：同时遍历两个列表，函数接收两个参数
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(lambda x, y: x + y, a, b))   # 对应位置相加
print("逐位相加：", sums)               # [11, 22, 33]

# ── 五、filter() ───────────────────────────────────────

print("\n── filter() ──")

# filter(函数, 可迭代对象)：保留函数返回 True 的元素，同样是惰性迭代器
numbers = range(-5, 6)                   # -5 到 5 的整数序列
positives = list(filter(lambda x: x > 0, numbers))  # 只保留正数
print("正数：", positives)              # [1, 2, 3, 4, 5]

# filter 传 None 时，过滤掉所有"假值"（0、None、""、[]、False 等）
mixed = [0, 1, "", "hello", None, [], [1, 2], False, True]
truthy = list(filter(None, mixed))       # None 表示"用元素本身判断真假"
print("真值元素：", truthy)             # [1, 'hello', [1, 2], True]

# 结合自定义函数过滤
def is_passing(score):                   # 判断是否及格
    return score >= 60                   # 返回布尔值

raw_scores = [88, 45, 72, 33, 91, 58]
passing = list(filter(is_passing, raw_scores))
print("及格分数：", passing)            # [88, 72, 91]

# ── 六、zip() ──────────────────────────────────────────

print("\n── zip() ──")

# zip(序列1, 序列2, ...)：把多个序列"拉链式"配对，长度以最短的为准
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 22]
cities = ["北京", "上海", "广州"]

# zip 生成惰性迭代器，用 list() 或 for 循环消耗
for name, age, city in zip(names, ages, cities):    # 同时解包三个序列
    print(f"  {name}，{age}岁，来自{city}")

# zip 配合 dict() 快速建字典
mapping = dict(zip(names, ages))         # 名字 -> 年龄
print("zip 建字典：", mapping)           # {'Alice': 25, 'Bob': 30, 'Charlie': 22}

# zip(*二维列表) 相当于矩阵转置（行列互换）
matrix = [[1, 2, 3], [4, 5, 6]]         # 2 行 3 列
transposed = list(zip(*matrix))          # * 把列表展开为多个参数
print("转置结果：", transposed)          # [(1, 4), (2, 5), (3, 6)]，3 行 2 列

# zip_longest：配对时补齐较短的序列（需从 itertools 导入）
from itertools import zip_longest        # 标准库，无需安装
short = [1, 2]
long_ = ["a", "b", "c", "d"]
padded = list(zip_longest(short, long_, fillvalue=0))  # 缺少的位置填 0
print("补齐配对：", padded)             # [(1, 'a'), (2, 'b'), (0, 'c'), (0, 'd')]

# ── 七、sorted() ───────────────────────────────────────

print("\n── sorted() ──")

# sorted(可迭代对象, key=函数, reverse=False)：返回新的已排序列表，原对象不变
# list.sort() 是原地排序，sorted() 是生成新列表
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print("升序：", sorted(nums))            # [1, 1, 2, 3, 4, 5, 6, 9]
print("降序：", sorted(nums, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]
print("原列表不变：", nums)              # [3, 1, 4, 1, 5, 9, 2, 6]

# key 参数：传入函数，按函数返回值排序，而非元素本身
words = ["banana", "apple", "cherry", "fig", "date"]
by_length = sorted(words, key=len)       # len 是内置函数，按字符串长度排序
print("按长度排序：", by_length)         # ['fig', 'date', 'apple', 'banana', 'cherry']

# 对字典列表排序：key 用 lambda 取字典中某个字段
products = [
    {"name": "键盘", "price": 299},
    {"name": "鼠标", "price": 89},
    {"name": "显示器", "price": 1599},
]
by_price = sorted(products, key=lambda p: p["price"])   # 按价格升序
for p in by_price:
    print(f"  {p['name']}: ¥{p['price']}")

# 多字段排序：key 返回元组，先按第一个字段，相同时按第二个
data = [("Bob", 90), ("Alice", 85), ("Charlie", 90), ("Alice", 80)]
multi = sorted(data, key=lambda x: (x[0], -x[1]))  # 按姓名升序，同名按分数降序
print("多字段排序：", multi)

# ── 八、enumerate() ────────────────────────────────────

print("\n── enumerate() ──")

# enumerate(可迭代对象, start=0)：同时返回索引和元素，避免手动维护计数器
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
for i, fruit in enumerate(fruits):       # i 从 0 开始
    print(f"  [{i}] {fruit}")

# start 参数让索引从指定值开始（常用于显示"第几名"）
print("排名：")
top3 = ["金牌", "银牌", "铜牌"]
for rank, medal in enumerate(top3, start=1):   # 从 1 开始计数
    print(f"  第{rank}名：{medal}")

# enumerate 配合推导式：生成 (索引, 值) 的字典
index_map = {i: v for i, v in enumerate(fruits)}   # 索引作键
print("索引字典：", index_map)           # {0: '苹果', 1: '香蕉', ...}

# ── 九、any() 和 all() ─────────────────────────────────

print("\n── any() 与 all() ──")

# any(可迭代对象)：只要有一个元素为真，就返回 True（短路求值）
# all(可迭代对象)：所有元素都为真，才返回 True（短路求值）

scores = [88, 45, 72, 91, 58]

# any：有没有人不及格（分数 < 60）
has_fail = any(s < 60 for s in scores)  # 生成器表达式作参数，不用 []
print("有人不及格：", has_fail)          # True（45 和 58）

# all：是否所有人都及格
all_pass = all(s >= 60 for s in scores) # 全部满足才是 True
print("全部及格：", all_pass)            # False

# 实用场景：检查列表是否有非空字符串
tags = ["python", "data", ""]           # 最后一个是空字符串
print("有空标签：", any(t == "" for t in tags))   # True
print("全非空：", all(t != "" for t in tags))     # False

# any/all 对空序列的行为：any([]) → False，all([]) → True（数学惯例）
print("any([]):", any([]))               # False（没有任何真值）
print("all([]):", all([]))               # True（没有任何假值，即"全部满足"）

# ── 十、生成器表达式 ───────────────────────────────────

print("\n── 生成器表达式 ──")

# 生成器表达式语法和列表推导式相同，把 [] 换成 ()
# 区别：列表推导式立即生成所有元素放入内存；生成器是惰性的，按需逐个产生

# 列表推导式：一次性把 100 万个平方存入内存
# big_list = [n ** 2 for n in range(1_000_000)]  # 占用大量内存

# 生成器表达式：只保存"生成规则"，几乎不占内存
big_gen = (n ** 2 for n in range(1_000_000))     # () 而非 []
print("生成器对象：", big_gen)           # <generator object ...>（还没计算）

# next() 手动取下一个值，生成器每次只计算一个
print("第1个：", next(big_gen))          # 0（0**2）
print("第2个：", next(big_gen))          # 1（1**2）
print("第3个：", next(big_gen))          # 4（2**2）

# for 循环消耗生成器：按需逐个取值，内存始终只存一个元素
gen = (n * 3 for n in range(5))          # 生成 0,3,6,9,12
for val in gen:                          # 每次循环取一个，用完丢弃
    print(val, end=" ")
print()

# 生成器可以直接传给 sum()、max() 等内置函数（无需先转 list）
total = sum(n ** 2 for n in range(1, 6)) # 1+4+9+16+25，括号可省略
print("平方和：", total)                 # 55

# 生成器只能遍历一次！遍历完后再次遍历得到空结果
gen2 = (x for x in range(3))
print("第一次遍历：", list(gen2))        # [0, 1, 2]
print("第二次遍历：", list(gen2))        # []（已耗尽，没有元素了）

# ── 综合示例：成绩分析流水线 ─────────────────────────

print("\n── 综合示例：成绩分析流水线 ──")

raw = [                                  # 原始数据：(姓名, 成绩) 元组列表
    ("小明", 88), ("小红", 45), ("小刚", 72),
    ("小李", 91), ("小王", 58), ("小张", 63),
]

# 第一步：用字典推导式建立 {姓名: 成绩} 映射
grade_map = {name: score for name, score in raw}
print("成绩字典：", grade_map)

# 第二步：filter 筛选及格学生（分数 >= 60）
passing_pairs = filter(lambda x: x[1] >= 60, raw)   # x 是 (名, 分) 元组

# 第三步：map 为每个及格学生打上等级标签
def grade_label(pair):                   # 接收 (名字, 分数) 元组
    name, score = pair                   # 解包元组
    level = "优秀" if score >= 85 else "良好" if score >= 70 else "及格"
    return f"{name}({level}:{score})"    # 返回格式化字符串

labeled = list(map(grade_label, passing_pairs))   # 批量生成标签
print("及格学生：", labeled)

# 第四步：sorted 按分数降序排列（需从原始 raw 中重新过滤）
ranked = sorted(
    [(name, score) for name, score in raw if score >= 60],  # 列表推导式过滤
    key=lambda x: x[1],                  # 按分数（元组第二个元素）排序
    reverse=True,                        # 降序（高分在前）
)
print("排名榜：")
for rank, (name, score) in enumerate(ranked, start=1):   # enumerate 加序号
    print(f"  第{rank}名：{name} — {score}分")

# 第五步：用 any/all 做整体判断
all_above_40 = all(s >= 40 for _, s in raw)   # _ 表示不关心的变量（姓名）
any_perfect   = any(s == 100 for _, s in raw) # 有没有满分
print("全部 >= 40 分：", all_above_40)   # True
print("有满分：", any_perfect)           # False

# 第六步：生成器表达式高效求平均（不生成中间列表）
avg = sum(s for _, s in raw) / len(raw)  # 生成器直接传给 sum()
print(f"班级平均分：{avg:.1f}")          # 保留一位小数
