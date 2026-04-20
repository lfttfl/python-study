# Python 数据结构练习：字典（dict）与集合（set）
# =====================================================

# ══════════════════════════════════════════════════════
# 一、字典基础
# ══════════════════════════════════════════════════════

# 字典用花括号 {} 定义，存储"键:值"对，键必须唯一且不可变，值可以是任意类型
# Python 3.7+ 字典保证插入顺序
person = {
    "name": "小明",                           # 键是字符串（最常见），值是字符串
    "age": 18,                                # 值可以是整数
    "scores": [88, 92, 79],                   # 值可以是列表
    "is_student": True,                       # 值可以是布尔值
}
empty_dict = {}                               # 空字典（注意：{} 是字典不是集合）
also_dict  = dict(name="小红", age=17)        # dict() 构造函数，键不加引号

print("字典：", person)
print("类型：", type(person))                 # <class 'dict'>
print("长度：", len(person))                  # 4，键值对的数量

# ── 1-1 查询（读取值）─────────────────────────────────

print("\n── 查询 ──")

# 方括号 [] 按键取值：键不存在时抛出 KeyError，生产代码要避免盲用
print(person["name"])                         # 小明
print(person["scores"])                       # [88, 92, 79]

# get(键, 默认值)：键不存在时返回默认值而非报错，更安全
print(person.get("age"))                      # 18
print(person.get("email"))                    # None（键不存在，返回默认 None）
print(person.get("email", "未填写"))          # 未填写（自定义默认值）

# in 关键字：检查键是否存在（只检查键，不检查值）
print("name" in person)                       # True
print("email" in person)                      # False
print("小明" in person)                       # False（"小明"是值，不是键）

# keys()、values()、items() 分别返回键视图、值视图、键值对视图
# 视图是"活的"：字典改变时视图自动更新
print("所有键：", list(person.keys()))        # ['name', 'age', 'scores', 'is_student']
print("所有值：", list(person.values()))      # ['小明', 18, [88, 92, 79], True]
print("键值对：", list(person.items()))       # [('name', '小明'), ('age', 18), ...]

# ── 1-2 增加与修改 ─────────────────────────────────────

print("\n── 增加与修改 ──")

profile = {"name": "小刚", "age": 19}

# 直接用 [] 赋值：键存在则修改，键不存在则新增
profile["city"] = "北京"                      # 新增键 "city"
print("新增后：", profile)                    # {'name': '小刚', 'age': 19, 'city': '北京'}

profile["age"] = 20                           # 修改已存在的键
print("修改后：", profile)                    # {'name': '小刚', 'age': 20, 'city': '北京'}

# update()：批量更新/新增键值对，接受字典或关键字参数
profile.update({"email": "gang@mail.com", "age": 21})  # age 被覆盖，email 被新增
print("update 后：", profile)

profile.update(hobby="编程", level="中级")   # 也可以直接用关键字参数
print("update(kw) 后：", profile)

# setdefault(键, 默认值)：键存在时什么都不做并返回已有值；键不存在时插入默认值并返回它
# 常用于"第一次见到就初始化"的场景，避免先判断再赋值的冗余
result = profile.setdefault("name", "匿名")  # "name" 已存在，不覆盖
print("setdefault 已有键：", result)          # 小刚（原值不变）

result2 = profile.setdefault("score", 0)     # "score" 不存在，插入 0
print("setdefault 新键：", result2)           # 0
print("插入后：", profile)

# ── 1-3 删除 ───────────────────────────────────────────

print("\n── 删除 ──")

data = {"a": 1, "b": 2, "c": 3, "d": 4}

# pop(键, 默认值)：删除并返回对应值；键不存在时返回默认值（不提供则报 KeyError）
val = data.pop("b")                           # 删除键 "b"，返回其值 2
print(f"pop('b') = {val}，剩余：{data}")

val2 = data.pop("z", -1)                     # 键不存在，返回默认值 -1，不报错
print(f"pop('z') = {val2}")                   # -1

# del 语句：按键删除，不返回值，键不存在报 KeyError
del data["c"]
print("del 后：", data)                       # {'a': 1, 'd': 4}

# popitem()：删除并返回最后插入的键值对（LIFO），字典为空时报 KeyError
last = data.popitem()                         # Python 3.7+ 保证是最后插入的那对
print("popitem()：", last, "剩余：", data)    # ('d', 4)，剩余 {'a': 1}

data2 = {"x": 10, "y": 20}
data2.clear()                                 # clear()：清空所有键值对，保留字典对象
print("clear() 后：", data2)                  # {}

# ── 1-4 遍历 ───────────────────────────────────────────

print("\n── 遍历 ──")

inventory = {"苹果": 50, "香蕉": 30, "橙子": 45}

# 直接 for 循环遍历：默认遍历键
for key in inventory:                         # 等同于 for key in inventory.keys()
    print(f"  键：{key}")

# 遍历值
for value in inventory.values():
    print(f"  值：{value}")

# 遍历键值对（最常用）：items() 返回 (键, 值) 元组，解包赋给两个变量
for fruit, count in inventory.items():        # 解包让代码更可读
    print(f"  {fruit}：库存 {count} 个")

# 带序号遍历：enumerate + items()
for i, (fruit, count) in enumerate(inventory.items(), start=1):
    print(f"  第{i}种：{fruit} × {count}")

# 字典推导式遍历并变换（复习）
doubled = {k: v * 2 for k, v in inventory.items()}   # 库存翻倍
print("翻倍库存：", doubled)

# ── 1-5 嵌套字典 ───────────────────────────────────────

print("\n── 嵌套字典 ──")

# 字典的值可以是另一个字典，形成嵌套结构（类似 JSON）
students = {
    "stu001": {"name": "小明", "age": 18, "grades": {"数学": 88, "英语": 92}},
    "stu002": {"name": "小红", "age": 17, "grades": {"数学": 95, "英语": 87}},
    "stu003": {"name": "小刚", "age": 19, "grades": {"数学": 72, "英语": 68}},
}

# 链式索引：一层一层往下取
print(students["stu001"]["name"])             # 小明
print(students["stu002"]["grades"]["数学"])   # 95

# 安全访问嵌套键：链式 get()，任一层不存在都返回 None 而不报错
math_score = students.get("stu999", {}).get("grades", {}).get("数学", "无记录")
print("不存在的学生数学分：", math_score)     # 无记录

# 遍历嵌套字典
for sid, info in students.items():
    avg = sum(info["grades"].values()) / len(info["grades"])   # 计算该生平均分
    print(f"  {sid} {info['name']}：平均 {avg:.1f} 分")

# 动态构建嵌套字典：setdefault 避免"先判断键是否存在"的冗余
word_positions = {}                           # 记录每个单词出现的位置
sentence = "the cat sat on the mat the cat"
for pos, word in enumerate(sentence.split()):
    word_positions.setdefault(word, []).append(pos)   # 键不存在就先建空列表再追加
print("词语位置：", word_positions)

# ── 1-6 其他实用方法与技巧 ────────────────────────────

print("\n── 其他技巧 ──")

# dict.fromkeys(键列表, 默认值)：用统一默认值批量建字典
keys = ["语文", "数学", "英语", "物理"]
scores_init = dict.fromkeys(keys, 0)          # 所有科目初始化为 0
print("fromkeys：", scores_init)

# 字典合并（Python 3.9+）：| 运算符
d1 = {"a": 1, "b": 2}
d2 = {"b": 99, "c": 3}                       # "b" 键冲突，右侧优先
merged = d1 | d2                              # 生成新字典，原字典不变
print("| 合并：", merged)                     # {'a': 1, 'b': 99, 'c': 3}

d1 |= d2                                      # |= 原地合并（修改 d1）
print("|= 原地合并：", d1)

# 用 zip 从两个列表快速建字典（复习）
names  = ["小明", "小红", "小刚"]
ages   = [18, 17, 19]
name_age = dict(zip(names, ages))
print("zip 建字典：", name_age)

# Counter：统计元素频次的特殊字典（继承自 dict）
from collections import Counter               # 标准库，无需安装
text = "abracadabra"
freq = Counter(text)                          # 统计每个字符出现次数
print("字符频次：", freq)                     # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print("最常见 3 个：", freq.most_common(3))   # [('a', 5), ('b', 2), ('r', 2)]

# defaultdict：访问不存在的键时自动生成默认值，避免 KeyError
from collections import defaultdict           # 标准库
dd = defaultdict(list)                        # 默认值工厂是 list，即默认生成 []
dd["fruits"].append("苹果")                   # 键 "fruits" 不存在，自动创建空列表再 append
dd["fruits"].append("香蕉")
dd["vegs"].append("胡萝卜")
print("defaultdict：", dict(dd))

# ══════════════════════════════════════════════════════
# 二、集合（set）
# ══════════════════════════════════════════════════════

print("\n══ 集合基础 ══")

# 集合用花括号 {} 定义，元素无序、不重复、元素必须可哈希（不可变）
# 主要用途：去重、成员检测（比列表快）、集合运算
fruits_set = {"苹果", "香蕉", "橙子", "苹果"}  # "苹果" 重复，自动去掉
print("集合（自动去重）：", fruits_set)         # {'苹果', '香蕉', '橙子'}（顺序不固定）
print("类型：", type(fruits_set))               # <class 'set'>

# 注意：空集合必须用 set()，不能用 {}（{} 是空字典）
empty_set = set()                              # 正确：空集合
print("空集合：", empty_set, type(empty_set))  # set() <class 'set'>

# set() 把其他可迭代对象转换为集合（常用于列表去重）
dup_list = [1, 2, 2, 3, 3, 3, 4]
unique = set(dup_list)                         # 转集合去重
print("去重：", unique)                        # {1, 2, 3, 4}
back_to_list = sorted(unique)                  # 转回有序列表（集合无序，sort 前先 sorted）
print("去重后的列表：", back_to_list)

# frozenset：不可变集合，可以作为字典的键或放入另一个集合
fs = frozenset([1, 2, 3])                     # 创建后不能增删元素
print("frozenset：", fs)

# ── 2-1 增加与删除 ─────────────────────────────────────

print("\n── 集合增删 ──")

s = {"a", "b", "c"}

s.add("d")                                    # add()：添加单个元素，已存在则忽略
print("add('d')：", s)

s.add("a")                                    # 添加已存在元素，集合不变
print("add('a') 无变化：", s)

s.update(["e", "f", "a"])                     # update()：批量添加（接受任意可迭代对象）
print("update 后：", s)                        # 'a' 已存在会被忽略

s.remove("b")                                 # remove()：删除元素，不存在则报 KeyError
print("remove('b')：", s)

s.discard("z")                                # discard()：删除元素，不存在时静默忽略（不报错）
print("discard('z') 安全：", s)               # 集合不变

popped = s.pop()                              # pop()：随机删除并返回一个元素（集合无序）
print(f"pop() 弹出 '{popped}'，剩余：", s)

s.clear()                                     # clear()：清空集合
print("clear() 后：", s)                      # set()

# ── 2-2 集合运算 ───────────────────────────────────────

print("\n── 集合运算 ──")

A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

# 并集（union）：A 或 B 中的所有元素（去重）
print("并集 A|B：", A | B)                    # {1, 2, 3, 4, 5, 6, 7, 8}
print("并集 A.union(B)：", A.union(B))        # 等价写法，更语义化

# 交集（intersection）：A 和 B 都有的元素
print("交集 A&B：", A & B)                    # {4, 5}
print("交集 A.intersection(B)：", A.intersection(B))

# 差集（difference）：在 A 中但不在 B 中的元素（注意顺序！）
print("差集 A-B：", A - B)                    # {1, 2, 3}（A 有 B 没有）
print("差集 B-A：", B - A)                    # {6, 7, 8}（B 有 A 没有）
print("差集 A.difference(B)：", A.difference(B))

# 对称差集（symmetric_difference）：A 或 B 有但不同时拥有的元素
print("对称差 A^B：", A ^ B)                  # {1, 2, 3, 6, 7, 8}
print("对称差方法：", A.symmetric_difference(B))

# 原地运算：直接修改集合本身（节省内存）
C = {1, 2, 3}
C |= {3, 4, 5}                               # 原地并集
print("|= 原地并集：", C)                     # {1, 2, 3, 4, 5}

D = {1, 2, 3, 4}
D &= {2, 3, 5}                               # 原地交集
print("&= 原地交集：", D)                     # {2, 3}

# ── 2-3 关系判断 ───────────────────────────────────────

print("\n── 关系判断 ──")

small = {1, 2, 3}
big   = {1, 2, 3, 4, 5}
other = {6, 7, 8}

# 子集：small 的所有元素都在 big 中
print("small ⊆ big：", small.issubset(big))   # True
print("small <= big：", small <= big)          # 等价写法

# 真子集：子集且不相等
print("small < big：", small < big)            # True（small 是 big 的真子集）
print("big < big：", big < big)                # False（相等不是真子集）

# 超集：big 包含 small 的所有元素
print("big ⊇ small：", big.issuperset(small)) # True
print("big >= small：", big >= small)          # 等价写法

# 不相交：两个集合没有共同元素
print("small∩other=∅：", small.isdisjoint(other))  # True（没有共同元素）
print("small∩big=∅：",  small.isdisjoint(big))     # False（有共同元素）

# in 检测：集合的成员检测比列表快得多（O(1) vs O(n)）
print("3 in small：", 3 in small)             # True
print("9 in small：", 9 in small)             # False

# ══════════════════════════════════════════════════════
# 三、字典 vs 集合：使用场景对比
# ══════════════════════════════════════════════════════

print("\n══ 字典 vs 集合 ══")

# ┌──────────────┬──────────────────────────┬──────────────────────────┐
# │              │ 字典 dict                │ 集合 set                 │
# ├──────────────┼──────────────────────────┼──────────────────────────┤
# │ 存储内容     │ 键值对（key → value）    │ 单值（只有键，无值）     │
# │ 有序性       │ 保证插入顺序（3.7+）     │ 无序                     │
# │ 重复         │ 键唯一，值可重复         │ 元素唯一                 │
# │ 查找速度     │ O(1) 按键查找            │ O(1) 成员检测            │
# │ 典型场景     │ 映射关系、计数、缓存     │ 去重、集合运算、快速查找 │
# └──────────────┴──────────────────────────┴──────────────────────────┘

# 场景 1：用字典做缓存（记忆化），避免重复计算
cache = {}                                    # 字典作为缓存容器
def fibonacci(n):
    if n in cache:                            # 先查缓存
        return cache[n]
    if n <= 1:
        return n
    result = fibonacci(n - 1) + fibonacci(n - 2)
    cache[n] = result                         # 计算结果存入缓存
    return result

print("Fibonacci(10)：", fibonacci(10))       # 55，缓存大幅提升性能
print("Fibonacci(30)：", fibonacci(30))       # 832040

# 场景 2：用集合做快速成员检测（黑名单/白名单）
banned_users = {"spam_bot", "troll_123", "fake_account"}   # 集合，O(1) 查找

def can_post(username):
    return username not in banned_users       # 集合查找比列表快得多

print("小明可以发帖：", can_post("小明"))     # True
print("troll可以发帖：", can_post("troll_123"))  # False

# 场景 3：用字典统计词频（Counter 的手动实现原理）
words_list = ["python", "is", "great", "python", "is", "fun", "python"]
word_count = {}
for word in words_list:
    word_count[word] = word_count.get(word, 0) + 1  # get 取已有值，键不存在返回 0
print("词频统计：", word_count)

# 场景 4：用集合做数据去重与集合运算（找共同好友）
alice_friends = {"Bob", "Charlie", "David", "Eve"}
bob_friends   = {"Alice", "Charlie", "Frank", "Eve"}

common   = alice_friends & bob_friends        # 共同好友
only_alice = alice_friends - bob_friends      # Alice 独有的好友
all_known  = alice_friends | bob_friends      # 所有认识的人
print("共同好友：", common)
print("Alice 独有好友：", only_alice)
print("所有认识的人：", all_known)

# ── 综合示例：学生选课系统 ────────────────────────────

print("\n── 综合示例：学生选课系统 ──")

# 用字典存学生信息，值中用集合存已选课程（集合自动去重且查找快）
course_system = {
    "小明": {"courses": {"数学", "英语", "物理"}, "gpa": 3.5},
    "小红": {"courses": {"数学", "化学", "生物"}, "gpa": 3.8},
    "小刚": {"courses": {"英语", "历史", "地理"}, "gpa": 3.2},
}

# 新增选课：集合 add()，天然防止重复选课
course_system["小明"]["courses"].add("化学")
print("小明选课后：", course_system["小明"]["courses"])

# 退课：discard() 不报错，更安全
course_system["小刚"]["courses"].discard("历史")
print("小刚退课后：", course_system["小刚"]["courses"])

# 查找选了"数学"的所有学生（用集合推导式）
math_students = {name for name, info in course_system.items()
                 if "数学" in info["courses"]}  # in 对集合是 O(1) 查找
print("选了数学的学生：", math_students)

# 找出小明和小红都选的课程（集合交集）
common_courses = (course_system["小明"]["courses"]
                  & course_system["小红"]["courses"])
print("小明∩小红共同课程：", common_courses)

# 所有开设的课程（各学生课程的并集）
all_courses = set()                           # 初始化空集合
for info in course_system.values():
    all_courses |= info["courses"]            # 原地并集，逐步合并
print("全部课程：", sorted(all_courses))      # sorted 让输出有序

# 按 GPA 降序输出学生信息（字典 + 排序）
print("\nGPA 排名：")
ranked = sorted(course_system.items(),
                key=lambda x: x[1]["gpa"],    # 按嵌套字典中的 gpa 字段排序
                reverse=True)
for rank, (name, info) in enumerate(ranked, start=1):
    print(f"  第{rank}名：{name}  GPA={info['gpa']}  "
          f"课程={sorted(info['courses'])}")   # sorted 使集合以稳定顺序显示
