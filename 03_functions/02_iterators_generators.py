# Python 函数进阶练习：迭代器与生成器
# =====================================================

import itertools                              # 标准库：高效迭代工具集
import sys                                    # 用于查看内存占用

# ══════════════════════════════════════════════════════
# 一、迭代协议基础
# ══════════════════════════════════════════════════════

print("══ 一、迭代协议基础 ══")

# Python 的 for 循环底层做了三件事：
#   1. 调用 iter(obj)  → 得到一个迭代器对象
#   2. 反复调用 next(迭代器) → 依次取出每个值
#   3. 捕获 StopIteration 异常 → 循环结束

nums = [10, 20, 30]                           # 列表是"可迭代对象"（iterable），但不是迭代器
it = iter(nums)                               # iter() 调用 nums.__iter__()，返回列表迭代器
print(type(it))                               # <class 'list_iterator'>

print(next(it))                               # 10，调用 it.__next__()，指针向前移动
print(next(it))                               # 20
print(next(it))                               # 30
try:
    next(it)                                  # 超出末尾，抛出 StopIteration
except StopIteration:
    print("迭代器耗尽，抛出 StopIteration")

# for 循环等价的手写版本
print("\nfor 循环的手写等价：")
it2 = iter([1, 2, 3])                         # 第一步：获取迭代器
while True:                                   # 第二步：无限循环
    try:
        value = next(it2)                     # 第三步：取下一个值
        print(value, end=" ")
    except StopIteration:                     # 第四步：捕获结束信号退出循环
        break
print()

# 可迭代对象 vs 迭代器 的区别：
# 可迭代对象（Iterable）：有 __iter__ 方法，每次 iter() 返回新迭代器（可多次遍历）
# 迭代器（Iterator）：同时有 __iter__ 和 __next__，只能单向前进，不能重置
lst = [1, 2, 3]                               # 可迭代对象
it_a = iter(lst)                              # 迭代器 A
it_b = iter(lst)                              # 迭代器 B（独立的，互不干扰）
print(next(it_a), next(it_a))                 # 1 2（A 前进了两步）
print(next(it_b))                             # 1（B 还在起点）

# 迭代器的 __iter__ 返回自身（迭代器本身也是可迭代的）
it3 = iter([7, 8, 9])
print(it3 is iter(it3))                       # True：iter(迭代器) 返回自身

# ══════════════════════════════════════════════════════
# 二、自定义迭代器
# ══════════════════════════════════════════════════════

print("\n══ 二、自定义迭代器 ══")

# ── 2-1 用类实现迭代器：__iter__ + __next__ ───────────

class CountUp:                                # 从 start 数到 stop 的计数器迭代器
    """从 start 开始，每次加 step，直到超过 stop"""

    def __init__(self, start, stop, step=1):
        self.current = start                  # 当前值，初始等于 start
        self.stop    = stop                   # 上限（包含）
        self.step    = step                   # 步长

    def __iter__(self):                       # 返回迭代器本身（让对象同时是可迭代的）
        return self

    def __next__(self):                       # 每次调用 next() 都会执行这里
        if self.current > self.stop:          # 超过上限，发出结束信号
            raise StopIteration
        value = self.current                  # 记录当前值
        self.current += self.step             # 指针前进
        return value                          # 返回当前值

print("CountUp(1, 5)：", end="")
for n in CountUp(1, 5):                      # for 循环自动调用 __iter__ 和 __next__
    print(n, end=" ")
print()

print("CountUp(0, 10, 2)：", end="")         # 步长为 2
for n in CountUp(0, 10, 2):
    print(n, end=" ")
print()

# 支持 list()、sum() 等任何接受可迭代对象的内置函数
print("list(CountUp(1,5))：", list(CountUp(1, 5)))
print("sum(CountUp(1,5))： ", sum(CountUp(1, 5)))   # 1+2+3+4+5=15

# ── 2-2 分离可迭代对象与迭代器（更严格的设计）─────────

class FibSequence:                            # 可迭代对象：代表"斐波那契数列"这个概念
    """斐波那契数列，最多产出 n 项"""
    def __init__(self, n):
        self.n = n                            # 保存最大项数

    def __iter__(self):                       # 每次 for 循环都创建全新的迭代器
        return FibIterator(self.n)            # 返回独立的迭代器对象，支持多次遍历

class FibIterator:                            # 迭代器：持有遍历状态
    def __init__(self, n):
        self.n     = n                        # 最大项数
        self.count = 0                        # 已产出项数
        self.a, self.b = 0, 1                 # 相邻两项

    def __iter__(self):                       # 迭代器的 __iter__ 返回自身
        return self

    def __next__(self):
        if self.count >= self.n:              # 已产出 n 项，结束
            raise StopIteration
        value    = self.a                     # 当前项
        self.a, self.b = self.b, self.a + self.b   # 滚动更新
        self.count += 1
        return value

fib5 = FibSequence(5)
print("斐波那契前5项：", list(fib5))          # [0, 1, 1, 2, 3]
print("再次遍历：    ", list(fib5))           # [0, 1, 1, 2, 3]（FibSequence 可重复遍历）

# 对比：迭代器本身只能遍历一次
fib_it = FibIterator(5)
print("迭代器第一次：", list(fib_it))         # [0, 1, 1, 2, 3]
print("迭代器第二次：", list(fib_it))         # []（已耗尽，空列表）

# ── 2-3 无限迭代器 ────────────────────────────────────

print("\n── 无限迭代器 ──")

class InfiniteCounter:                        # 从 start 无限自增的迭代器
    def __init__(self, start=0):
        self.n = start

    def __iter__(self):
        return self

    def __next__(self):                       # 永远不抛出 StopIteration
        value = self.n
        self.n += 1
        return value                          # 无限序列

counter = InfiniteCounter(1)
# 必须用 break 或 islice 限制取值，否则无限循环
first5 = [next(counter) for _ in range(5)]   # 手动取 5 个
print("无限计数器前5个：", first5)            # [1, 2, 3, 4, 5]

# ══════════════════════════════════════════════════════
# 三、生成器函数（Generator Function）
# ══════════════════════════════════════════════════════

print("\n══ 三、生成器函数 ══")

# 生成器函数：包含 yield 关键字的函数
# 调用生成器函数不会立即执行函数体，而是返回一个生成器对象
# 每次调用 next() 时，函数体才从上次暂停处继续执行，直到下一个 yield

# ── 3-1 yield 基础 ────────────────────────────────────

def simple_gen():                             # 这是一个生成器函数（因为含有 yield）
    print("  [gen] 开始执行")
    yield 1                                   # 暂停，把 1 返回给调用方，函数状态保留
    print("  [gen] 从 yield 1 后继续")
    yield 2                                   # 再次暂停，返回 2
    print("  [gen] 从 yield 2 后继续")
    yield 3                                   # 再次暂停，返回 3
    print("  [gen] 函数体结束，自动抛出 StopIteration")

print("── yield 基础 ──")
g = simple_gen()                              # 调用生成器函数：返回生成器对象，函数体未执行
print("生成器对象：", g)                      # <generator object simple_gen at ...>
print("取第1个：", next(g))                   # 开始执行到第一个 yield，返回 1
print("取第2个：", next(g))                   # 继续执行到第二个 yield，返回 2
print("取第3个：", next(g))                   # 继续执行到第三个 yield，返回 3
try:
    next(g)                                   # 函数体结束，自动抛出 StopIteration
except StopIteration:
    print("  [主程序] 捕获到 StopIteration")

# 生成器同样是迭代器，可以直接用 for 循环
print("\nfor 循环消耗生成器：")
for val in simple_gen():                      # 每次 for 循环都创建全新的生成器对象
    print(val, end=" ")
print()

# ── 3-2 生成器 vs 列表的内存对比 ─────────────────────

print("\n── 内存对比 ──")

def gen_range(n):                             # 生成器版的 range：按需产出，不占额外内存
    i = 0
    while i < n:
        yield i                               # 每次产出一个值就暂停
        i += 1

N = 1_000_000
list_mem = sys.getsizeof(list(range(N)))      # 列表：一次性存入内存
gen_mem  = sys.getsizeof(gen_range(N))        # 生成器：只存储函数状态

print(f"列表占用内存：{list_mem:,} 字节 ({list_mem // 1024 // 1024} MB)")
print(f"生成器占用内存：{gen_mem} 字节（与 N 无关，始终很小）")

# ── 3-3 实用生成器函数 ────────────────────────────────

print("\n── 实用生成器 ──")

def fibonacci_gen():                          # 无限斐波那契生成器（不用担心内存）
    a, b = 0, 1
    while True:                               # 无限循环，靠调用方决定取多少个
        yield a                               # 产出当前值后暂停
        a, b = b, a + b                       # 更新状态，下次 next() 时继续

def take(n, iterable):                        # 辅助函数：从可迭代对象取前 n 个
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item                            # 也是生成器：节省内存

fib = fibonacci_gen()                         # 无限斐波那契流
print("斐波那契前10项：", list(take(10, fib)))  # [0,1,1,2,3,5,8,13,21,34]

def read_chunks(text, chunk_size=5):          # 按固定大小分块读取（模拟大文件分块）
    """把长文本按 chunk_size 切成小块，逐块产出"""
    for i in range(0, len(text), chunk_size): # 步长 chunk_size，每次跳 chunk_size 个字符
        yield text[i : i + chunk_size]        # 切片取当前块

sample = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print("分块读取（每块5字符）：", list(read_chunks(sample, 5)))

def running_average():                        # 协程风格：接受数据并持续计算均值
    """用 send() 喂数据，yield 产出当前均值"""
    total, count = 0, 0
    while True:
        value = yield (total / count if count else None)   # 先产出当前均值，再等待接收
        if value is None:                     # send(None) 表示结束（也是 next() 的效果）
            return
        total += value
        count += 1

avg_gen = running_average()
next(avg_gen)                                 # 必须先 next() 启动生成器，执行到第一个 yield
print("发送10：", avg_gen.send(10))           # 发送10，得到当前均值 10.0
print("发送20：", avg_gen.send(20))           # 发送20，得到均值 15.0
print("发送30：", avg_gen.send(30))           # 发送30，得到均值 20.0

# ── 3-4 生成器的 send()、throw()、close() ─────────────

print("\n── 生成器双向通信 ──")

def echo_gen():                               # 双向生成器：用 send() 传值，yield 接收并返回
    print("  [echo] 启动，等待输入")
    while True:
        received = yield                       # yield 右边没有值时产出 None；左边接收 send() 的值
        if received is None:                  # next() 等价于 send(None)
            continue
        print(f"  [echo] 收到 '{received}'，转为大写后返回")
        yield received.upper()               # 产出处理后的值

eg = echo_gen()
next(eg)                                      # 启动：运行到第一个 yield，暂停
print(eg.send("hello"))                       # 发送 "hello"，运行到第二个 yield，返回 "HELLO"
next(eg)                                      # 消耗掉第二个 yield，回到循环顶部等待
print(eg.send("world"))                       # 发送 "world"，返回 "WORLD"
eg.close()                                    # 关闭生成器：在暂停处抛出 GeneratorExit

# ══════════════════════════════════════════════════════
# 四、yield from
# ══════════════════════════════════════════════════════

print("\n══ 四、yield from ══")

# yield from 可迭代对象：等价于对可迭代对象中每个元素执行 yield
# 但比手写 for + yield 更高效，且能正确处理 send()/throw()/close() 等信号

# ── 4-1 yield from 展开嵌套序列 ──────────────────────

def chain_simple(*iterables):                 # 手写版：多层 for + yield
    for it in iterables:
        for item in it:                       # 两层循环才能展开
            yield item

def chain_yf(*iterables):                     # yield from 版：更简洁
    for it in iterables:
        yield from it                         # 自动把 it 的每个元素逐一产出

print("chain_simple：", list(chain_simple([1,2], [3,4], [5,6])))
print("chain_yf：    ", list(chain_yf([1,2], [3,4], [5,6])))    # 结果相同

# yield from 也接受任意可迭代对象
def flatten(nested):                          # 递归展开任意深度的嵌套列表
    for item in nested:
        if isinstance(item, list):            # 如果元素还是列表，递归展开
            yield from flatten(item)          # yield from 递归：把子列表的所有元素透传出去
        else:
            yield item                        # 非列表直接产出

deep = [1, [2, [3, [4, [5]]]]]
print("深度展开：", list(flatten(deep)))      # [1, 2, 3, 4, 5]

complex_nested = [1, [2, 3], [4, [5, 6]], [[7], 8]]
print("复杂嵌套：", list(flatten(complex_nested)))   # [1, 2, 3, 4, 5, 6, 7, 8]

# ── 4-2 yield from 的返回值（子生成器的 return 值）────

def sub_gen():                                # 子生成器
    yield 1
    yield 2
    return "子生成器完成"                     # 生成器函数的 return 值会变成 StopIteration 的 value

def delegating_gen():                         # 委托生成器
    result = yield from sub_gen()             # yield from 会捕获子生成器的 return 值
    print(f"  [委托] 子生成器返回了：'{result}'")  # "子生成器完成"
    yield 99                                  # 委托结束后继续产出自己的值

print("── yield from 返回值 ──")
for v in delegating_gen():
    print(v, end=" ")                         # 1 2（来自子生成器）99（来自委托生成器）
print()

# ── 4-3 生成器管道 ────────────────────────────────────

print("\n── 生成器管道 ──")

# 生成器管道：多个生成器串联，数据像水流一样逐个通过每个阶段
# 优点：惰性求值，任意时刻内存中只有一个数据项，适合处理超大数据集

def data_source(items):                       # 阶段0：数据源（模拟读取日志文件）
    """逐行产出数据"""
    for item in items:
        yield item

def stage_strip(stream):                      # 阶段1：清理空白
    for line in stream:
        stripped = line.strip()
        if stripped:                          # 过滤掉空行
            yield stripped

def stage_parse(stream):                      # 阶段2：解析成结构化字典
    for line in stream:
        parts = line.split("|")              # 按 | 分割字段
        if len(parts) == 3:                  # 只处理格式正确的行
            yield {"level": parts[0].strip(),
                   "time":  parts[1].strip(),
                   "msg":   parts[2].strip()}

def stage_filter_errors(stream):              # 阶段3：只保留 ERROR 级别日志
    for record in stream:
        if record["level"] == "ERROR":
            yield record

def stage_format(stream):                     # 阶段4：格式化为可读字符串
    for record in stream:
        yield f"[{record['time']}] {record['msg']}"

# 模拟日志数据
raw_logs = [
    "INFO  | 10:00:01 | 服务器启动",
    "DEBUG | 10:00:02 | 配置加载完成",
    "ERROR | 10:00:03 | 数据库连接失败",
    "  ",                                     # 空行
    "INFO  | 10:00:05 | 重试连接...",
    "ERROR | 10:00:06 | 磁盘空间不足",
    "INFO  | 10:00:07 | 备份任务完成",
    "ERROR | 10:00:09 | 内存溢出",
]

# 串联管道：每个阶段的输出直接作为下一阶段的输入
# 整个管道是惰性的：只有当最终消费时，数据才一条条流过所有阶段
pipeline = stage_format(
    stage_filter_errors(
        stage_parse(
            stage_strip(
                data_source(raw_logs)
            )
        )
    )
)

print("ERROR 日志：")
for line in pipeline:                         # 此时才真正开始执行所有阶段
    print(" ", line)

# ══════════════════════════════════════════════════════
# 五、itertools 常用工具
# ══════════════════════════════════════════════════════

print("\n══ 五、itertools 工具 ══")

# itertools 提供高效的迭代器构建工具，全部是惰性的（按需计算）

# ── 5-1 chain：把多个可迭代对象串联成一个 ─────────────

print("\n── itertools.chain ──")

# chain(*iterables)：依次产出每个可迭代对象的元素，像拼接一样
combined = list(itertools.chain([1, 2], [3, 4], "56", (7, 8)))
print("chain：", combined)                    # [1, 2, 3, 4, '5', '6', 7, 8]

# chain.from_iterable：接受一个"可迭代的可迭代对象"，效果与 chain(*) 相同
nested_lists = [[1, 2], [3, 4], [5, 6]]
flat = list(itertools.chain.from_iterable(nested_lists))  # 比 chain(*) 更省内存
print("chain.from_iterable：", flat)          # [1, 2, 3, 4, 5, 6]

# 实用场景：合并多个分批查询结果
batch1 = [{"id": 1}, {"id": 2}]
batch2 = [{"id": 3}, {"id": 4}]
batch3 = [{"id": 5}]
all_records = list(itertools.chain(batch1, batch2, batch3))
print("合并批次：", all_records)

# ── 5-2 islice：对迭代器做切片（不支持负索引）─────────

print("\n── itertools.islice ──")

# islice(iterable, stop) 或 islice(iterable, start, stop, step)
# 像列表切片，但适用于任意迭代器（包括无限迭代器）

def naturals():                               # 无限自然数生成器
    n = 1
    while True:
        yield n
        n += 1

# 从无限序列中取前10个（如果用 list() 会死循环）
first10 = list(itertools.islice(naturals(), 10))
print("前10个自然数：", first10)              # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# islice(start, stop, step)
every3rd = list(itertools.islice(naturals(), 0, 20, 3))   # 0-20之间每隔3取一个
print("每3个取1个(0-20)：", every3rd)         # [1, 4, 7, 10, 13, 16, 19]

# 跳过前 N 个（通过 start 参数）
skip5 = list(itertools.islice(range(20), 5, 10))  # 跳过前5，取5到9
print("跳过前5取5个：", skip5)               # [5, 6, 7, 8, 9]

# ── 5-3 product：笛卡尔积 ─────────────────────────────

print("\n── itertools.product ──")

# product(*iterables, repeat=1)：计算多个序列的笛卡尔积
# 等价于多层嵌套 for 循环，但更简洁

# 两个序列的笛卡尔积（等价于两层 for）
colors = ["红", "绿"]
sizes  = ["S", "M", "L"]
combos = list(itertools.product(colors, sizes))
print("颜色×尺码：", combos)
# [('红','S'),('红','M'),('红','L'),('绿','S'),('绿','M'),('绿','L')]

# repeat 参数：同一序列自身做笛卡尔积
dice = list(itertools.product(range(1, 4), repeat=2))  # 两个骰子（1-3）的所有组合
print("骰子组合（1-3）×2：", dice)
print(f"共 {len(dice)} 种组合")               # 3^2 = 9

# 三个序列的组合
stocks = list(itertools.product(["买入", "卖出"], [10, 20], ["A股", "港股"]))
print(f"交易组合数：{len(stocks)}")            # 2×2×2 = 8

# 实用场景：枚举所有密码组合（小规模，演示原理）
import string
digits = string.digits                         # "0123456789"
two_digit_pins = list(itertools.product(digits, repeat=2))   # 两位数字密码
print(f"两位数字密码共 {len(two_digit_pins)} 种")  # 10^2 = 100

# ── 5-4 combinations 和 permutations ──────────────────

print("\n── 组合与排列 ──")

letters = ["A", "B", "C", "D"]

# combinations(iterable, r)：从 r 个元素中取 r 个，不重复，不考虑顺序
combos2 = list(itertools.combinations(letters, 2))
print(f"C(4,2)={len(combos2)} 种组合：", combos2)

# permutations(iterable, r)：从中取 r 个，不重复，考虑顺序
perms = list(itertools.permutations(letters, 2))
print(f"P(4,2)={len(perms)} 种排列：", perms)

# combinations_with_replacement：可重复选取
combos_rep = list(itertools.combinations_with_replacement("AB", 3))
print("可重复组合 C+R('AB',3)：", combos_rep)  # AA…BB

# ── 5-5 groupby：对连续相同 key 的元素分组 ────────────

print("\n── itertools.groupby ──")

# groupby(iterable, key=None)：把相邻的、key 相同的元素归为一组
# ⚠️ 重要：groupby 只对连续相邻的相同 key 分组，使用前必须先排序！

data = [
    {"name": "小明", "dept": "技术"},
    {"name": "小红", "dept": "技术"},
    {"name": "小刚", "dept": "市场"},
    {"name": "小李", "dept": "市场"},
    {"name": "小王", "dept": "技术"},   # 注意：未排序时"技术"被拆为两组
]

# 错误示范：未排序直接 groupby（"技术"出现两次，会被分为两组）
print("未排序 groupby（错误示范）：")
for dept, members in itertools.groupby(data, key=lambda x: x["dept"]):
    print(f"  {dept}：{[m['name'] for m in members]}")
# 会出现两个"技术"组！

# 正确做法：先按 key 排序，再 groupby
print("\n排序后 groupby（正确）：")
sorted_data = sorted(data, key=lambda x: x["dept"])   # 先排序
for dept, members in itertools.groupby(sorted_data, key=lambda x: x["dept"]):
    member_list = [m["name"] for m in members]        # members 是迭代器，只能消费一次
    print(f"  {dept}：{member_list}")

# 统计每部门人数
print("\n各部门人数：")
sorted_data2 = sorted(data, key=lambda x: x["dept"])
dept_count = {dept: len(list(members))
              for dept, members in itertools.groupby(sorted_data2, key=lambda x: x["dept"])}
print(dept_count)

# groupby 按数字区间分组（需要自定义 key 函数）
scores = sorted([88, 45, 72, 91, 63, 55, 79, 95, 38, 67])  # 必须先排序
def score_band(s):                            # key 函数：分数转等级区间
    return "优秀" if s >= 90 else "良好" if s >= 70 else "及格" if s >= 60 else "不及格"

print("\n成绩分组（需先排序 key）：")
# groupby 按字符串分组，必须先用 key 排序，再 groupby 同一 key
for band, members in itertools.groupby(sorted(scores, key=score_band), key=score_band):
    print(f"  {band}：{list(members)}")

# ── 5-6 其他常用 itertools ───────────────────────────

print("\n── 其他 itertools ──")

# count(start, step)：无限计数（比自定义 InfiniteCounter 简洁）
counter_it = itertools.count(10, 5)          # 从 10 开始，步长 5
print("count(10,5) 前5个：", list(itertools.islice(counter_it, 5)))   # [10,15,20,25,30]

# cycle(iterable)：无限循环重复一个序列
cycler = itertools.cycle(["A", "B", "C"])    # 无限循环 A B C A B C ...
print("cycle 前8个：", list(itertools.islice(cycler, 8)))  # ['A','B','C','A','B','C','A','B']

# repeat(value, times)：重复产出同一值
print("repeat：", list(itertools.repeat("X", 4)))  # ['X', 'X', 'X', 'X']

# takewhile(predicate, iterable)：条件为真时持续取，一旦为假立刻停止
print("takewhile <5：", list(itertools.takewhile(lambda x: x < 5, [1, 2, 3, 6, 4, 2])))
# [1, 2, 3]（遇到 6 就停了，后面的 4 2 也被忽略）

# dropwhile(predicate, iterable)：条件为真时跳过，一旦为假就开始取
print("dropwhile <5：", list(itertools.dropwhile(lambda x: x < 5, [1, 2, 3, 6, 4, 2])))
# [6, 4, 2]（前面小于5的被跳过，从第一个 >=5 的元素开始取到末尾）

# starmap：像 map，但参数从元组中解包后传给函数
pairs = [(2, 3), (4, 2), (10, 0.5)]
print("starmap pow：", list(itertools.starmap(pow, pairs)))   # [8, 16, 3.162...]

# zip_longest：配对，较短的序列用 fillvalue 补齐（比内置 zip 更灵活）
a = [1, 2, 3, 4]
b = ["x", "y"]
print("zip_longest：", list(itertools.zip_longest(a, b, fillvalue="-")))
# [(1,'x'),(2,'y'),(3,'-'),(4,'-')]

# ══════════════════════════════════════════════════════
# 六、综合示例：惰性 ETL 数据管道
# ══════════════════════════════════════════════════════

print("\n══ 六、综合示例：惰性 ETL 管道 ══")

# 模拟从多个数据源读取日志（chain），惰性处理，最终统计

def gen_logs(source_id, count):               # 生成器：模拟从某数据源读取日志
    levels = itertools.cycle(["INFO", "WARN", "ERROR"])  # 循环产出级别
    src_num = ord(source_id) - ord("A") + 1   # 把字母转成数字：A=1, B=2, C=3
    for i, level in zip(range(count), levels):
        yield {"src": source_id, "seq": i + 1,
               "level": level,
               "val": (i + 1) * (src_num * 10)}    # 纯数值字段，便于排序比较

def enrich(stream):                           # 生成器：为每条记录添加"是否告警"字段
    for rec in stream:
        rec["alert"] = rec["level"] in ("WARN", "ERROR")  # 级别不是 INFO 就告警
        yield rec

def only_alerts(stream):                      # 生成器：过滤，只保留告警记录
    yield from (rec for rec in stream if rec["alert"])   # yield from + 生成器表达式

def top_n(stream, n, key):                    # 生成器：取 key 最大的前 n 条
    # 因为需要全局比较，必须消耗完流，是管道中唯一需要全量数据的阶段
    yield from sorted(stream, key=key, reverse=True)[:n]

# 构建多源数据管道
source_a = gen_logs("A", 6)                   # 数据源 A：6 条
source_b = gen_logs("B", 4)                   # 数据源 B：4 条
source_c = gen_logs("C", 5)                   # 数据源 C：5 条

all_logs  = itertools.chain(source_a, source_b, source_c)  # 合并三路来源
enriched  = enrich(all_logs)                   # 添加告警标记
alerts    = only_alerts(enriched)              # 过滤出告警
top_alerts = top_n(alerts, 5, key=lambda r: r["val"])      # 取 val 最大的 5 条

print(f"{'来源':^4} {'序号':^4} {'级别':^6} {'值':>6}")
print("-" * 26)
for rec in top_alerts:
    print(f"{rec['src']:^4} {rec['seq']:^4} {rec['level']:^6} {rec['val']:>6}")
print("（以上是所有告警中 val 最大的 5 条）")

# 用 groupby 按来源统计告警数（需重新生成，迭代器已耗尽）
def count_alerts_by_source():
    all_src = itertools.chain(gen_logs("A", 6), gen_logs("B", 4), gen_logs("C", 5))
    alert_list = list(only_alerts(enrich(all_src)))   # 告警列表（需要排序故转 list）
    alert_list.sort(key=lambda r: r["src"])            # 先按来源排序
    print("\n各来源告警数：")
    for src, grp in itertools.groupby(alert_list, key=lambda r: r["src"]):
        print(f"  {src}：{len(list(grp))} 条")

count_alerts_by_source()
