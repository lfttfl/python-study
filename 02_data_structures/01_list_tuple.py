# Python 数据结构练习：列表（list）与元组（tuple）
# =====================================================

# ══════════════════════════════════════════════════════
# 一、列表基础
# ══════════════════════════════════════════════════════

# 列表用方括号 [] 定义，元素可以是任意类型，允许重复，有序可变
fruits = ["苹果", "香蕉", "橙子", "葡萄"]   # 字符串列表
mixed  = [1, "hello", 3.14, True, None]      # 混合类型列表（合法但少用）
empty  = []                                   # 空列表，后续动态添加元素

print("原始列表：", fruits)
print("列表长度：", len(fruits))              # len() 返回元素数量
print("类型：", type(fruits))                 # <class 'list'>

# ── 1-1 索引与查询 ─────────────────────────────────────

print("\n── 索引与查询 ──")

print(fruits[0])                              # 正向索引：0 是第一个元素
print(fruits[-1])                             # 负向索引：-1 是最后一个元素
print(fruits[-2])                             # -2 是倒数第二个

# in 关键字：检查元素是否存在，返回布尔值
print("香蕉 in fruits:", "香蕉" in fruits)    # True
print("芒果 in fruits:", "芒果" in fruits)    # False

# index() 返回第一个匹配元素的索引，找不到则抛出 ValueError
print("橙子的索引：", fruits.index("橙子"))   # 2

# count() 统计某元素出现次数
nums = [1, 2, 2, 3, 2, 4]
print("2 出现次数：", nums.count(2))          # 3

# ── 1-2 切片 ───────────────────────────────────────────

print("\n── 切片 ──")

# 切片语法：列表[start:stop:step]，取 start 到 stop-1，间隔 step
letters = ["a", "b", "c", "d", "e", "f", "g"]

print(letters[1:4])                           # ['b', 'c', 'd']，不含索引 4
print(letters[:3])                            # ['a', 'b', 'c']，start 省略默认 0
print(letters[4:])                            # ['e', 'f', 'g']，stop 省略默认到末尾
print(letters[::2])                           # ['a', 'c', 'e', 'g']，步长 2（隔一取一）
print(letters[::-1])                          # ['g', 'f', 'e', 'd', 'c', 'b', 'a']，步长 -1 反转
print(letters[1:-1])                          # ['b', 'c', 'd', 'e', 'f']，去掉首尾

# 切片赋值：直接替换一段元素（列表独有，元组不支持）
letters[2:4] = ["C", "D"]                    # 把索引 2、3 的元素替换
print("切片赋值后：", letters)               # ['a', 'b', 'C', 'D', 'e', 'f', 'g']

# ── 1-3 增加元素 ───────────────────────────────────────

print("\n── 增加元素 ──")

colors = ["红", "绿"]

colors.append("蓝")                           # append()：在末尾追加单个元素，原地修改
print("append 后：", colors)                  # ['红', '绿', '蓝']

colors.insert(1, "黄")                        # insert(索引, 值)：在指定位置插入，后面元素后移
print("insert 后：", colors)                  # ['红', '黄', '绿', '蓝']

colors.extend(["紫", "橙"])                   # extend()：把另一个列表的所有元素追加进来
print("extend 后：", colors)                  # ['红', '黄', '绿', '蓝', '紫', '橙']

# + 运算符：拼接两个列表，生成新列表，原列表不变
new_colors = colors + ["白", "黑"]
print("+ 拼接：", new_colors)

# * 运算符：重复列表元素，生成新列表
repeated = [0] * 5                            # 生成 [0, 0, 0, 0, 0]
print("* 重复：", repeated)

# ── 1-4 删除元素 ───────────────────────────────────────

print("\n── 删除元素 ──")

items = ["a", "b", "c", "d", "e"]

items.remove("c")                             # remove(值)：删除第一个匹配值，找不到报 ValueError
print("remove('c')：", items)                 # ['a', 'b', 'd', 'e']

popped = items.pop()                          # pop()：弹出并返回最后一个元素
print("pop() 弹出：", popped, "→ 剩余：", items)   # 弹出 'e'

popped_idx = items.pop(0)                     # pop(索引)：弹出指定索引的元素
print("pop(0) 弹出：", popped_idx, "→ 剩余：", items)  # 弹出 'a'

del items[0]                                  # del 语句：按索引删除，不返回值
print("del [0] 后：", items)                  # ['d']

backup = ["x", "y", "x", "z", "x"]
backup.clear()                                # clear()：清空列表，保留列表对象本身
print("clear() 后：", backup)                 # []

# ── 1-5 修改元素 ───────────────────────────────────────

print("\n── 修改元素 ──")

scores = [70, 85, 60, 95, 78]
scores[2] = 65                                # 直接用索引赋值修改指定位置的元素
print("修改索引 2：", scores)                 # [70, 85, 65, 95, 78]

scores[0:2] = [75, 88]                        # 切片赋值：批量修改多个元素
print("切片修改：", scores)                   # [75, 88, 65, 95, 78]

# ── 1-6 排序 ───────────────────────────────────────────

print("\n── 排序 ──")

nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sort()：原地排序，直接修改列表，返回 None
nums.sort()                                   # 默认升序
print("sort() 升序：", nums)                  # [1, 1, 2, 3, 4, 5, 6, 9]

nums.sort(reverse=True)                       # reverse=True 改为降序
print("sort() 降序：", nums)                  # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted()：不修改原列表，返回新的已排序列表
original = [5, 2, 8, 1]
new_sorted = sorted(original)                 # 原列表不变
print("sorted()：", new_sorted, "| 原列表：", original)

# key 参数：按自定义规则排序
words = ["banana", "apple", "cherry", "fig"]
words.sort(key=len)                           # 按字符串长度升序
print("按长度排序：", words)                  # ['fig', 'apple', 'banana', 'cherry']

# reverse()：原地翻转列表（不排序，只是倒序）
nums2 = [1, 2, 3, 4, 5]
nums2.reverse()
print("reverse()：", nums2)                   # [5, 4, 3, 2, 1]

# ── 1-7 嵌套列表（二维列表）──────────────────────────

print("\n── 嵌套列表 ──")

# 列表的元素本身也可以是列表，形成二维（或更高维）结构
matrix = [                                    # 3 行 3 列的矩阵
    [1, 2, 3],                                # 第 0 行
    [4, 5, 6],                                # 第 1 行
    [7, 8, 9],                                # 第 2 行
]

print(matrix[1])                              # [4, 5, 6]，取第 1 行
print(matrix[1][2])                           # 6，取第 1 行第 2 列（行索引在前）

# 遍历二维列表：双层 for 循环
for row in matrix:                            # 外层遍历每一行
    for val in row:                           # 内层遍历行内每个元素
        print(val, end="\t")                  # \t 是制表符，对齐输出
    print()                                   # 每行结束换行

# 修改二维列表中的某个元素
matrix[0][0] = 99                             # 修改第 0 行第 0 列
print("修改后第 0 行：", matrix[0])           # [99, 2, 3]

# 浅拷贝陷阱：直接赋值只复制引用，修改会相互影响
a = [[1, 2], [3, 4]]
b = a                                         # b 和 a 指向同一个对象
b[0][0] = 99
print("a 被连带修改：", a)                    # [[99, 2], [3, 4]]

# 用 copy 模块的 deepcopy() 实现真正的深拷贝
import copy                                   # 导入标准库 copy 模块
c = copy.deepcopy(a)                          # 深拷贝：递归复制所有层级
c[0][0] = 0
print("deepcopy 后 a 不变：", a)              # [[99, 2], [3, 4]]，a 不受影响

# ── 1-8 其他常用操作 ───────────────────────────────────

print("\n── 其他常用操作 ──")

nums3 = [4, 2, 7, 1, 9]
print("最大值：", max(nums3))                 # 9
print("最小值：", min(nums3))                 # 1
print("求和：", sum(nums3))                   # 23

# list() 把其他可迭代对象转换为列表
print("range 转列表：", list(range(5)))       # [0, 1, 2, 3, 4]
print("字符串转列表：", list("hello"))        # ['h', 'e', 'l', 'l', 'o']

# join()：把字符串列表拼接成一个字符串（注意是字符串方法，不是列表方法）
words2 = ["Hello", "World", "Python"]
print("-".join(words2))                       # Hello-World-Python（用 - 连接）
print(" ".join(words2))                       # Hello World Python（用空格连接）

# ══════════════════════════════════════════════════════
# 二、元组（tuple）
# ══════════════════════════════════════════════════════

print("\n══ 元组基础 ══")

# 元组用圆括号 () 定义，有序，但创建后不可修改（不可变序列）
point  = (3, 7)                               # 二维坐标点
colors = ("红", "绿", "蓝")                   # 三元素元组
single = (42,)                                # 单元素元组：末尾必须加逗号，否则只是括号
empty_t = ()                                  # 空元组

print("元组：", colors)
print("类型：", type(point))                  # <class 'tuple'>
print("单元素：", single, "类型：", type(single))   # (42,) <class 'tuple'>

# 也可以不写括号，直接用逗号分隔，Python 自动识别为元组
auto_tuple = 1, 2, 3                          # 括号可省略，逗号是关键
print("省略括号：", auto_tuple, type(auto_tuple))   # (1, 2, 3) <class 'tuple'>

# ── 2-1 元组的不可变性 ─────────────────────────────────

print("\n── 不可变性 ──")

t = (10, 20, 30)
print(t[0])                                   # 可以读取（索引、切片都支持）
print(t[1:])                                  # (20, 30)，切片返回新元组

# t[0] = 99                                   # 取消注释会报 TypeError：元组不支持赋值
# t.append(40)                                # 取消注释会报 AttributeError：元组无 append 方法

# 元组支持的操作：len、index、count、in、+、*
print("长度：", len(t))                       # 3
print("20 的索引：", t.index(20))             # 1
print("拼接：", t + (40, 50))                 # (10, 20, 30, 40, 50)，生成新元组
print("重复：", (0,) * 3)                     # (0, 0, 0)

# ── 2-2 解包（unpacking）─────────────────────────────

print("\n── 元组解包 ──")

# 解包：把元组（或列表）的元素分别赋给多个变量，数量必须匹配
x, y = (3, 7)                                 # 把 3 赋给 x，7 赋给 y
print(f"x={x}, y={y}")

# 交换两个变量的值：Python 的经典写法，底层利用元组解包
a, b = 10, 20
a, b = b, a                                   # 右侧先打包成 (20, 10)，再解包赋值
print(f"交换后 a={a}, b={b}")                 # a=20, b=10

# 星号 * 收集剩余元素（扩展解包）
first, *rest = [1, 2, 3, 4, 5]               # first=1，rest 收集剩余
print(f"first={first}, rest={rest}")          # first=1, rest=[2, 3, 4, 5]

*head, last = [1, 2, 3, 4, 5]                # head 收集前面的，last=5
print(f"head={head}, last={last}")            # head=[1, 2, 3, 4], last=5

first2, *middle, last2 = [1, 2, 3, 4, 5]    # 首尾各取一个，中间全收
print(f"first={first2}, middle={middle}, last={last2}")

# 嵌套解包：解构嵌套结构
(p, q), r = (1, 2), 3                        # 左侧结构与右侧匹配即可
print(f"p={p}, q={q}, r={r}")                # p=1, q=2, r=3

# 函数返回多值本质上是元组解包
def get_range(data):
    return min(data), max(data)              # 返回元组 (最小, 最大)

lo, hi = get_range([3, 1, 7, 2])            # 解包赋值
print(f"min={lo}, max={hi}")                 # min=1, max=7

# ── 2-3 命名元组（namedtuple）────────────────────────

print("\n── 命名元组 ──")

from collections import namedtuple           # 从标准库 collections 导入

# namedtuple('类型名', '字段列表')：创建一个有字段名的元组类
# 比普通元组可读性更高，比字典更轻量，仍然不可变
Point = namedtuple("Point", ["x", "y"])      # 定义二维坐标点类型
p1 = Point(3, 7)                             # 创建实例，像函数一样调用
p2 = Point(x=10, y=20)                       # 也支持关键字传参

print(p1)                                    # Point(x=3, y=7)
print(p1.x, p1.y)                            # 3 7，用属性名访问，比 p1[0] 更清晰
print(p1[0], p1[1])                          # 3 7，同样支持索引访问（兼容普通元组）

# _asdict()：转换为字典，方便序列化或调试
print(p1._asdict())                          # {'x': 3, 'y': 7}

# _replace()：返回修改了指定字段的新实例（原实例不变，保持不可变性）
p3 = p1._replace(y=100)                      # 只改 y，x 保持不变
print(f"p1={p1}, p3={p3}")                   # p1=Point(x=3,y=7), p3=Point(x=3,y=100)

# 实用示例：用命名元组表示结构化数据
Student = namedtuple("Student", ["name", "age", "score"])
students = [
    Student("小明", 18, 88),
    Student("小红", 17, 92),
    Student("小刚", 19, 75),
]
# 按分数排序，字段名让代码意图一目了然
for stu in sorted(students, key=lambda s: s.score, reverse=True):
    print(f"  {stu.name}（{stu.age}岁）：{stu.score}分")

# ══════════════════════════════════════════════════════
# 三、列表 vs 元组：使用场景对比
# ══════════════════════════════════════════════════════

print("\n══ 列表 vs 元组 ══")

# ┌──────────────┬──────────────────────┬──────────────────────┐
# │              │ 列表 list            │ 元组 tuple           │
# ├──────────────┼──────────────────────┼──────────────────────┤
# │ 可变性       │ 可变（增删改）       │ 不可变               │
# │ 性能         │ 略慢（需维护动态数组）│ 略快（固定内存布局） │
# │ 内存占用     │ 较多                 │ 较少                 │
# │ 哈希         │ 不可哈希（不能作字典键）│ 可哈希（元素全不可变时）│
# │ 语义         │ 同质数据的集合        │ 异质字段的记录        │
# └──────────────┴──────────────────────┴──────────────────────┘

# 内存对比：元组比列表占用内存更少
import sys                                   # sys 模块提供系统相关工具
lst = [1, 2, 3, 4, 5]
tpl = (1, 2, 3, 4, 5)
print(f"list  内存：{sys.getsizeof(lst)} 字节")   # 通常 120 字节左右
print(f"tuple 内存：{sys.getsizeof(tpl)} 字节")   # 通常  80 字节左右

# 元组可以作为字典的键（因为可哈希），列表不行
location_map = {}
location_map[(39.9, 116.4)] = "北京"        # (纬度, 经度) 元组作键
location_map[(31.2, 121.5)] = "上海"
print("坐标字典：", location_map)

# list_key = {[1,2]: "error"}              # 取消注释报 TypeError：list 不可哈希

# 使用原则：
# ✅ 用列表  → 需要增删改的同类数据集合（如购物车商品、日志条目）
# ✅ 用元组  → 固定结构的记录（如坐标、RGB 颜色、数据库行）
# ✅ 用命名元组 → 需要字段名提升可读性，但不需要方法的轻量对象

# ── 综合示例：学生成绩管理 ────────────────────────────

print("\n── 综合示例：学生成绩管理 ──")

# 用列表存储学生记录（需要增删），用元组存储每条记录（字段固定）
roster = [                                   # 花名册：列表（可变，可增删学生）
    ("小明", 18, [88, 92, 79]),              # 每个学生：元组（不变的身份信息）+ 列表（可变的成绩）
    ("小红", 17, [95, 87, 91]),
    ("小刚", 19, [72, 68, 80]),
]

# 新增一个学生
roster.append(("小李", 18, [85, 90, 88]))   # 向列表追加新元组

# 统计每位学生的平均分并排序
results = []
for name, age, grades in roster:            # 解包元组：三个变量对应三个字段
    avg = sum(grades) / len(grades)          # 列表的平均值
    results.append((name, round(avg, 1)))    # 存成 (姓名, 平均分) 元组

results.sort(key=lambda r: r[1], reverse=True)   # 按平均分降序排列

print("排名：")
for rank, (name, avg) in enumerate(results, start=1):   # 解包 + enumerate
    print(f"  第{rank}名：{name} — 平均 {avg} 分")
