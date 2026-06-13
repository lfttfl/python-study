# Python 标准库：collections 进阶 + heapq + bisect
# =====================================================

from collections import (
    Counter, defaultdict, deque, OrderedDict, ChainMap, namedtuple
)
import heapq
import bisect

# ══════════════════════════════════════════════════════
# 一、Counter：计数器
# ══════════════════════════════════════════════════════

print("══ 一、Counter ══")

# Counter 是字典的子类，专门用于计数
# 访问不存在的键返回 0（而不是 KeyError）

text = "abracadabra"
c = Counter(text)
print(f"字符计数：{c}")                         # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print(f"'a' 出现次数：{c['a']}")                # 5
print(f"'z' 出现次数：{c['z']}")                # 0（不存在返回 0，不报错）
print(f"最常见 3 个：{c.most_common(3)}")       # [('a', 5), ('b', 2), ('r', 2)]

# 统计单词频次
words = "the quick brown fox jumps over the lazy dog the fox".split()
word_freq = Counter(words)
print(f"\n词频：{word_freq}")
print(f"前3高频词：{word_freq.most_common(3)}")

# Counter 支持算术运算
c1 = Counter(["a", "b", "b", "c"])
c2 = Counter(["b", "b", "b", "d"])

print(f"\nc1 = {c1}")
print(f"c2 = {c2}")
print(f"c1 + c2 = {c1 + c2}")                  # 合并（计数相加）
print(f"c1 - c2 = {c1 - c2}")                  # 差集（只保留正数）
print(f"c1 & c2 = {c1 & c2}")                  # 交集（取较小值）
print(f"c1 | c2 = {c1 | c2}")                  # 并集（取较大值）

# elements()：按计数重复元素
print(f"c1 元素：{sorted(c1.elements())}")      # ['a', 'b', 'b', 'c']

# update / subtract
c1.update(["a", "a"])                           # 追加计数
print(f"update 后 c1['a'] = {c1['a']}")         # 3

# 实用场景：统计成绩分布
grades = [88, 92, 75, 88, 95, 75, 88, 62, 92, 75]
grade_dist = Counter(grades)
print(f"\n成绩分布：{dict(sorted(grade_dist.items()))}")

# ══════════════════════════════════════════════════════
# 二、defaultdict：带默认值的字典
# ══════════════════════════════════════════════════════

print("\n══ 二、defaultdict ══")

# defaultdict(default_factory)：访问不存在的键时，自动调用 default_factory() 创建默认值
# 避免"先判断键是否存在再赋值"的冗余代码

# ── list 作为默认工厂 ──
print("\n── defaultdict(list) ──")

# 普通字典需要判断键是否存在
word_positions_plain = {}
sentence = "the cat sat on the mat the cat"
for pos, word in enumerate(sentence.split()):
    if word not in word_positions_plain:        # 需要先判断
        word_positions_plain[word] = []
    word_positions_plain[word].append(pos)

# defaultdict 自动创建空列表
word_positions = defaultdict(list)
for pos, word in enumerate(sentence.split()):
    word_positions[word].append(pos)            # 键不存在时自动创建 []

print(f"词语位置：{dict(word_positions)}")

# 按字母分组单词
by_letter = defaultdict(list)
words2 = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
for w in words2:
    by_letter[w[0]].append(w)
for letter in sorted(by_letter):
    print(f"  {letter}: {by_letter[letter]}")

# ── int 作为默认工厂（计数）──
print("\n── defaultdict(int) ──")

# 手动实现 Counter 的原理
inventory = defaultdict(int)
sales = ["苹果", "香蕉", "苹果", "橙子", "苹果", "香蕉"]
for item in sales:
    inventory[item] += 1                       # 键不存在时默认值是 0
print(f"销售统计：{dict(inventory)}")

# ── set 作为默认工厂 ──
print("\n── defaultdict(set) ──")

# 每个用户关注的标签（自动去重）
user_tags = defaultdict(set)
interactions = [
    ("Alice", "Python"), ("Bob", "Java"), ("Alice", "Data"),
    ("Alice", "Python"),                        # 重复，集合自动去重
    ("Bob", "Python"), ("Carol", "Data"),
]
for user, tag in interactions:
    user_tags[user].add(tag)
for user, tags in sorted(user_tags.items()):
    print(f"  {user}: {sorted(tags)}")

# ── 嵌套 defaultdict ──
print("\n── 嵌套 defaultdict ──")

# 二维计数表（行 × 列）
matrix = defaultdict(lambda: defaultdict(int))  # lambda 返回新的 defaultdict(int)
data_pairs = [("A", "X"), ("A", "Y"), ("B", "X"), ("A", "X"), ("B", "Z")]
for row, col in data_pairs:
    matrix[row][col] += 1

for row in sorted(matrix):
    print(f"  {row}: {dict(matrix[row])}")

# ══════════════════════════════════════════════════════
# 三、deque：双端队列
# ══════════════════════════════════════════════════════

print("\n══ 三、deque ══")

# deque（double-ended queue）：两端都支持 O(1) 的插入和删除
# list 在头部插入/删除是 O(n)；deque 在头尾操作都是 O(1)

d = deque([1, 2, 3, 4, 5])
print(f"初始：{d}")

d.append(6)                                    # 右端追加 O(1)
d.appendleft(0)                                # 左端追加 O(1)
print(f"append/appendleft 后：{d}")

right = d.pop()                                # 右端弹出 O(1)
left  = d.popleft()                            # 左端弹出 O(1)
print(f"pop={right}, popleft={left}，剩余：{d}")

# extend / extendleft
d.extend([7, 8])                               # 右端批量追加
d.extendleft([-2, -1])                         # 左端批量追加（注意顺序是反的）
print(f"extend 后：{d}")

# rotate：旋转（正数向右，负数向左）
d2 = deque([1, 2, 3, 4, 5])
d2.rotate(2)                                   # 向右旋转 2 步
print(f"rotate(2)：{d2}")                       # [4, 5, 1, 2, 3]
d2.rotate(-1)                                  # 向左旋转 1 步
print(f"rotate(-1)：{d2}")                      # [5, 1, 2, 3, 4]

# maxlen：固定大小的滑动窗口（满了之后新元素入队会自动淘汰最旧的元素）
print("\n── 滑动窗口 ──")
recent = deque(maxlen=3)                       # 最多保留 3 个元素
for val in [1, 2, 3, 4, 5, 6]:
    recent.append(val)
    print(f"  加入 {val}：{list(recent)}")

# 实用场景：BFS（广度优先搜索）中的队列
print("\n── BFS 示例 ──")
def bfs(graph, start):
    visited = set()
    queue   = deque([start])
    order   = []
    while queue:
        node = queue.popleft()                 # 从左端取，O(1)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        queue.extend(graph.get(node, []))      # 邻居从右端入队
    return order

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [], "E": [], "F": []
}
print(f"BFS 遍历顺序：{bfs(graph, 'A')}")      # A B C D E F

# ══════════════════════════════════════════════════════
# 四、ChainMap：链式字典查找
# ══════════════════════════════════════════════════════

print("\n══ 四、ChainMap ══")

# ChainMap：把多个字典"链"在一起，查找时按顺序在各字典中搜索
# 写操作只影响第一个字典
# 典型场景：配置覆盖（命令行 > 环境变量 > 配置文件 > 默认值）

defaults  = {"color": "black", "size": 12, "font": "Arial", "bold": False}
user_prefs = {"color": "blue", "size": 14}
session   = {"bold": True}

# 查找优先级：session > user_prefs > defaults
config = ChainMap(session, user_prefs, defaults)

print(f"color = {config['color']}")            # blue（user_prefs 覆盖了 defaults）
print(f"font  = {config['font']}")             # Arial（只在 defaults 里）
print(f"bold  = {config['bold']}")             # True（session 覆盖了 defaults）

# 写操作只修改第一个字典
config["size"] = 16
print(f"修改后 session：{dict(session)}")       # {'bold': True, 'size': 16}
print(f"user_prefs 未变：{user_prefs}")

# new_child()：创建子上下文（在链的最前面插入新字典）
child_config = config.new_child({"color": "red"})
print(f"子上下文 color = {child_config['color']}")   # red
print(f"父上下文 color = {config['color']}")          # blue（父上下文不受影响）

# maps 属性：查看所有字典
print(f"字典数量：{len(config.maps)}")

# ══════════════════════════════════════════════════════
# 五、heapq：堆队列（优先队列）
# ══════════════════════════════════════════════════════

print("\n══ 五、heapq ══")

# heapq 实现最小堆（min-heap）：堆顶始终是最小元素，push/pop 都是 O(log n)
# Python 没有内置最大堆，用负数技巧实现

nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
heap = nums.copy()
heapq.heapify(heap)                            # 原地转为堆，O(n)
print(f"堆化后：{heap}")                        # [1, 1, 2, 3, 5, 9, 4, 6, 5, 3]（堆结构）

heapq.heappush(heap, 0)                        # 插入，O(log n)
print(f"插入 0 后堆顶：{heap[0]}")             # 0（最小值在堆顶）

smallest = heapq.heappop(heap)                 # 弹出最小值，O(log n)
print(f"弹出最小值：{smallest}")               # 0

# nlargest / nsmallest：取 N 个最大/最小值，比 sorted 更高效（当 n << len(data) 时）
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"最大的 3 个：{heapq.nlargest(3, data)}")   # [9, 6, 5]
print(f"最小的 3 个：{heapq.nsmallest(3, data)}")  # [1, 1, 2]

# 带优先级的任务队列
print("\n── 优先队列 ──")

tasks = []
# (优先级, 序号, 任务名)：序号保证相同优先级的任务按入队顺序排列
heapq.heappush(tasks, (3, 0, "低优先级任务"))
heapq.heappush(tasks, (1, 1, "高优先级任务"))
heapq.heappush(tasks, (2, 2, "中优先级任务"))
heapq.heappush(tasks, (1, 3, "另一个高优先级"))

while tasks:
    priority, _, task = heapq.heappop(tasks)
    print(f"  处理（优先级 {priority}）：{task}")

# ══════════════════════════════════════════════════════
# 六、bisect：二分查找与有序列表插入
# ══════════════════════════════════════════════════════

print("\n══ 六、bisect ══")

# bisect 维护有序列表，插入新元素时保持排序，查找用二分，O(log n)

sorted_list = [1, 3, 5, 7, 9, 11]

# bisect_left / bisect_right：找到插入位置（不实际插入）
pos_left  = bisect.bisect_left(sorted_list, 6)   # 找到 6 应该在哪里（左侧）
pos_right = bisect.bisect_right(sorted_list, 5)  # 找到 5 的右侧插入位置
print(f"bisect_left(6) = {pos_left}")            # 3（在索引 3 插入保持有序）
print(f"bisect_right(5) = {pos_right}")          # 3（5 的右侧）

# insort：插入并保持排序
bisect.insort(sorted_list, 6)                    # O(n)（移动元素），但查找是 O(log n)
print(f"insort(6) 后：{sorted_list}")            # [1, 3, 5, 6, 7, 9, 11]

# 实用场景：成绩转等级（二分查找分界点）
print("\n── 成绩等级转换 ──")

breakpoints = [60, 70, 80, 90]                  # 分界点（有序）
grades      = ["不及格", "及格", "良好", "优良", "优秀"]

def get_grade(score):
    # bisect_right 找到 score 在 breakpoints 中的插入位置，即对应等级的索引
    return grades[bisect.bisect_right(breakpoints, score)]

for score in [55, 60, 75, 85, 95, 100]:
    print(f"  {score} 分 → {get_grade(score)}")

# ══════════════════════════════════════════════════════
# 七、综合示例：文本频率分析
# ══════════════════════════════════════════════════════

print("\n══ 七、综合示例：文本频率分析 ══")

import re

def analyze_text(text):
    """综合使用 Counter、defaultdict、heapq 分析文本"""
    # 1. 分词（简单按非字母分隔）
    words3 = re.findall(r"[a-zA-Z']+", text.lower())

    # 2. 词频统计
    freq = Counter(words3)

    # 3. 按首字母分组（defaultdict）
    by_initial = defaultdict(list)
    for word, count in freq.items():
        by_initial[word[0]].append((count, word))

    # 4. 每个字母组内按频次排序（heapq nlargest）
    top_by_initial = {}
    for letter, word_counts in sorted(by_initial.items()):
        top_by_initial[letter] = heapq.nlargest(3, word_counts)

    return freq, top_by_initial

sample_text = """
To be or not to be that is the question whether tis nobler in the mind to suffer
the slings and arrows of outrageous fortune or to take arms against a sea of troubles
"""

freq, top_by_initial = analyze_text(sample_text)
print(f"总词数：{sum(freq.values())}")
print(f"唯一词数：{len(freq)}")
print(f"\n最高频 5 词：{freq.most_common(5)}")
print("\n各首字母最高频词（前2）：")
for letter, words4 in list(top_by_initial.items())[:5]:
    print(f"  {letter}: {[(w, c) for c, w in words4[:2]]}")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("\n══ 练习题 ══")
print("""
1. 用 Counter 统计一段英文文本中每个单词的出现次数，
   输出频次最高的 10 个词，并计算词汇量（不重复的单词数）。

2. 用 defaultdict 实现一个简单的倒排索引：
   输入一组文档（字符串列表），构建 {词: [出现该词的文档索引列表]} 的字典。

3. 用 deque(maxlen=N) 实现滑动窗口最大值：
   给定列表 nums 和窗口大小 k，返回每个窗口的最大值列表。

4. 用 heapq 实现"合并 k 个有序列表"：
   输入 [[1,4,7],[2,5,8],[3,6,9]]，输出合并后的有序列表 [1,2,3,4,5,6,7,8,9]。

参考答案见下方注释：
""")

# # 答案4：合并 k 个有序列表
# def merge_k_sorted(lists):
#     heap = []
#     for i, lst in enumerate(lists):
#         if lst:
#             heapq.heappush(heap, (lst[0], i, 0))   # (值, 列表索引, 元素索引)
#     result = []
#     while heap:
#         val, list_idx, elem_idx = heapq.heappop(heap)
#         result.append(val)
#         next_idx = elem_idx + 1
#         if next_idx < len(lists[list_idx]):
#             heapq.heappush(heap, (lists[list_idx][next_idx], list_idx, next_idx))
#     return result
#
# print(merge_k_sorted([[1,4,7],[2,5,8],[3,6,9]]))   # [1,2,3,4,5,6,7,8,9]
