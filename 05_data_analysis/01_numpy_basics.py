# Python 数据分析练习：NumPy 基础
# =====================================================

import numpy as np                            # NumPy 是数值计算的核心库，惯例别名 np
import sys                                    # 用于查看内存大小对比

print(f"NumPy 版本：{np.__version__}")

# ══════════════════════════════════════════════════════
# 一、ndarray 创建
# ══════════════════════════════════════════════════════

# ndarray（N-dimensional array）是 NumPy 的核心数据结构
# 与 Python 列表的关键区别：
#   ① 所有元素必须是同一类型（dtype），存储紧凑，内存连续
#   ② 支持向量化运算（不用写循环），底层 C 实现，速度比纯 Python 快 10~100 倍
#   ③ 形状（shape）固定，不能像列表那样随意 append

print("\n══ 一、ndarray 创建 ══")

# ── 1-1 从 Python 列表/嵌套列表创建 ──────────────────

arr1d = np.array([1, 2, 3, 4, 5])            # 一维数组，NumPy 自动推断 dtype=int64
arr2d = np.array([[1, 2, 3],                  # 二维数组（矩阵），嵌套列表深度决定维数
                  [4, 5, 6],
                  [7, 8, 9]])
arr_float = np.array([1.0, 2.5, 3.7])        # 含小数 → 自动推断 dtype=float64
arr_typed  = np.array([1, 2, 3], dtype=np.float32)  # 显式指定 dtype，节省内存

print("一维数组：", arr1d)
print("二维数组：\n", arr2d)
print("dtype 自动推断：", arr1d.dtype)        # int64（64位整数）
print("显式 float32：",  arr_typed.dtype)     # float32（单精度浮点）

# 数组的基本属性
print(f"\n形状 shape：{arr2d.shape}")          # (3, 3)：3行3列，元组表示各维度大小
print(f"维数 ndim： {arr2d.ndim}")            # 2：二维
print(f"元素总数 size：{arr2d.size}")         # 9：3×3=9 个元素
print(f"单元素字节 itemsize：{arr2d.itemsize}")  # 8：int64 占 8 字节
print(f"总字节数 nbytes：{arr2d.nbytes}")     # 72：9×8=72 字节

# 对比 Python 列表的内存占用
py_list = list(range(1000))
np_arr  = np.arange(1000, dtype=np.int64)
print(f"\n1000 元素列表内存：{sys.getsizeof(py_list)} 字节")   # ~8056
print(f"1000 元素 ndarray：{np_arr.nbytes} 字节")              # 8000（更紧凑）

# ── 1-2 zeros / ones / full：填充特定值 ─────────────

print("\n── zeros / ones / full ──")

zeros3x4 = np.zeros((3, 4))                  # 全 0 矩阵，默认 dtype=float64
ones2x3  = np.ones((2, 3), dtype=np.int32)   # 全 1 矩阵，指定整数类型
full3x3  = np.full((3, 3), fill_value=7.0)   # 全 7.0 矩阵
eye4     = np.eye(4)                          # 4×4 单位矩阵（对角线为 1，其余为 0）
empty2x2 = np.empty((2, 2))                  # 未初始化的数组（值是内存垃圾，速度最快）

print("zeros(3,4):\n", zeros3x4)
print("ones(2,3) int32:\n", ones2x3)
print("full(3,3, 7.0):\n", full3x3)
print("eye(4):\n", eye4)

# zeros_like / ones_like：与已有数组同形状同类型
template = np.array([[1, 2], [3, 4]])
print("zeros_like:\n", np.zeros_like(template))   # 形状(2,2) dtype=int64，全0
print("ones_like:\n",  np.ones_like(template))    # 形状(2,2) dtype=int64，全1

# ── 1-3 arange：等差序列（类似 range，但返回 ndarray）──

print("\n── arange ──")

a = np.arange(10)                             # 0 到 9，步长 1（默认从 0 开始）
print("arange(10)：", a)                      # [0 1 2 3 4 5 6 7 8 9]

b = np.arange(1, 11)                          # 1 到 10（stop 不含）
print("arange(1,11)：", b)                    # [1 2 3 4 5 6 7 8 9 10]

c = np.arange(0, 1, 0.1)                     # 0.0 到 0.9，步长 0.1（支持浮点步长）
print("arange(0,1,0.1)：", c.round(1))       # round(1) 避免浮点精度问题的显示

d = np.arange(10, 0, -2)                     # 倒序，步长 -2
print("arange(10,0,-2)：", d)                # [10  8  6  4  2]

# ── 1-4 linspace：均匀间隔（指定元素数而非步长）────────

print("\n── linspace ──")

# linspace(start, stop, num)：在 [start, stop] 区间内均匀取 num 个点（含两端）
ls5 = np.linspace(0, 1, 5)                   # 0 到 1，均匀取 5 个点
print("linspace(0,1,5)：", ls5)              # [0.   0.25 0.5  0.75 1.  ]

ls10 = np.linspace(0, 2*np.pi, 10)          # 0 到 2π，取 10 个点（画正弦曲线常用）
print("linspace(0,2π,10)：", np.round(ls10, 3))

# endpoint=False：不含终点（此时等价于 arange 的效果，步长=range/num）
ls_no_end = np.linspace(0, 1, 5, endpoint=False)
print("endpoint=False：", ls_no_end)          # [0.  0.2 0.4 0.6 0.8]

# logspace：对数均匀间隔（基数默认 10）
log_space = np.logspace(0, 3, 4)             # 10^0=1, 10^1=10, 10^2=100, 10^3=1000
print("logspace(0,3,4)：", log_space)        # [   1.   10.  100. 1000.]

# ── 1-5 random：随机数组 ──────────────────────────────

print("\n── random ──")

rng = np.random.default_rng(seed=42)         # 推荐的新式随机数生成器，seed 保证可复现

rand_uniform = rng.random((3, 3))            # [0, 1) 均匀分布，shape=(3,3)
rand_int     = rng.integers(1, 101, size=10) # [1, 100] 整数，size=10
rand_normal  = rng.normal(loc=0, scale=1, size=(2, 4))  # 标准正态分布，均值0 标准差1
rand_choice  = rng.choice([10, 20, 30, 40], size=6, replace=True)  # 有放回随机抽样

print("均匀分布(3,3):\n", rand_uniform.round(3))
print("随机整数：", rand_int)
print("正态分布(2,4):\n", rand_normal.round(3))
print("随机抽样：", rand_choice)

# ── 1-6 reshape / flatten：改变形状 ──────────────────

print("\n── reshape / flatten ──")

base = np.arange(1, 13)                      # [1, 2, ..., 12]，一维，12个元素
print("原始一维：", base)

m3x4 = base.reshape(3, 4)                   # 重塑为 3×4 矩阵，元素总数必须不变（3×4=12）
print("reshape(3,4):\n", m3x4)

m2x2x3 = base.reshape(2, 2, 3)             # 三维数组：2个面，每面2行3列
print("reshape(2,2,3):\n", m2x2x3)

# reshape(-1, ...)：-1 表示让 NumPy 自动计算该维度的大小
auto = base.reshape(-1, 4)                   # -1 自动算出行数=3（12/4=3）
print("reshape(-1,4):\n", auto)

# flatten()：多维数组压平为一维（返回副本）
flat = m3x4.flatten()
print("flatten：", flat)                     # [1 2 3 4 5 6 7 8 9 10 11 12]

# ravel()：功能同 flatten，但尽量返回视图（不复制数据，更省内存）
raveled = m3x4.ravel()
print("ravel：", raveled)                    # 同 flatten，但可能共享内存

# ══════════════════════════════════════════════════════
# 二、数组运算与广播机制
# ══════════════════════════════════════════════════════

print("\n══ 二、数组运算与广播 ══")

# ── 2-1 元素级（逐元素）运算 ──────────────────────────

print("\n── 逐元素运算 ──")

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# 四则运算：自动对应位置逐元素计算，无需写循环（向量化）
print("a + b  =", a + b)                     # [11 22 33 44]
print("a - b  =", a - b)                     # [-9 -18 -27 -36]
print("a * b  =", a * b)                     # [10 40 90 160]
print("b / a  =", b / a)                     # [10. 10. 10. 10.]
print("b // a =", b // a)                    # [10 10 10 10]（整除）
print("a ** 2 =", a ** 2)                    # [1 4 9 16]（逐元素平方）
print("b % 3  =", b % 3)                     # [1 2 0 1]（逐元素取余）

# 数学函数：也是逐元素作用
angles = np.linspace(0, np.pi, 5)
print("sin：", np.sin(angles).round(3))      # [0. 0.707 1. 0.707 0.]
print("exp：", np.exp(np.array([0,1,2])).round(3))  # [1. 2.718 7.389]
print("log：", np.log(np.array([1, np.e, np.e**2])).round(3))  # [0. 1. 2.]
print("sqrt：", np.sqrt(np.array([1, 4, 9, 16])))   # [1. 2. 3. 4.]
print("abs：", np.abs(np.array([-3, -1, 0, 2, 4]))) # [3 1 0 2 4]

# 比较运算：返回布尔数组
c = np.array([1, 5, 3, 8, 2, 7])
print("c > 3：", c > 3)                      # [False True False True False True]
print("c == 3：", c == 3)                    # [False False True False False False]

# ── 2-2 矩阵运算 ──────────────────────────────────────

print("\n── 矩阵运算 ──")

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

print("A * B（逐元素积）:\n", A * B)          # 注意：* 是逐元素，不是矩阵乘法！

# 矩阵乘法（点积）：两种等价写法
print("A @ B（矩阵乘法）:\n", A @ B)          # @ 运算符（Python 3.5+ 推荐写法）
print("np.dot(A,B):\n", np.dot(A, B))        # 等价写法

# 转置：行列互换
print("A.T（转置）:\n", A.T)                 # A.T 或 A.transpose()

# 线性代数模块
print("行列式 det(A)：", np.linalg.det(A))   # ad - bc = 1×4 - 2×3 = -2
print("逆矩阵 inv(A):\n", np.linalg.inv(A).round(3))  # A × inv(A) = 单位矩阵
eigenvals, eigenvecs = np.linalg.eig(A)
print("特征值：", eigenvals.round(3))         # A 的特征值

# ── 2-3 广播机制（Broadcasting）────────────────────────

print("\n── 广播机制 ──")

# 广播规则：形状不同的数组相运算时，NumPy 会自动"扩展"较小的数组
# 规则：从尾部维度对齐，若某维度大小为 1 或该维度不存在，则沿该维度广播

# 标量与数组：最简单的广播（标量被视为形状 () 的 0 维数组）
arr = np.array([1, 2, 3, 4, 5])
print("arr + 10：", arr + 10)                # 10 广播到每个元素：[11 12 13 14 15]
print("arr * 2：",  arr * 2)                 # [2 4 6 8 10]

# 一维与二维广播：行向量沿行方向复制
matrix = np.array([[1, 2, 3],               # shape: (3, 3)
                   [4, 5, 6],
                   [7, 8, 9]])
row_vec = np.array([10, 20, 30])             # shape: (3,) → 广播为 (3, 3)，每行复制
print("matrix + row_vec:\n", matrix + row_vec)   # 每行分别加 [10, 20, 30]

col_vec = np.array([[100],                   # shape: (3, 1) → 广播为 (3, 3)，每列复制
                    [200],
                    [300]])
print("matrix + col_vec:\n", matrix + col_vec)   # 每列分别加 100、200、300

# 两个不同形状的一维数组广播为二维（外积/行列组合）
row = np.array([1, 2, 3])                    # shape: (3,)  → 广播为 (4, 3)
col = np.array([[1], [2], [3], [4]])         # shape: (4,1) → 广播为 (4, 3)
outer = row + col                            # 每行加不同的列偏移
print("外积广播:\n", outer)                  # 4×3 矩阵，outer[i,j] = row[j] + col[i]

# 广播的实际应用：归一化（每列减去均值，除以标准差）
data = np.array([[2.0, 4.0, 6.0],
                 [1.0, 5.0, 9.0],
                 [3.0, 3.0, 3.0]])
col_mean = data.mean(axis=0)                 # 每列的均值，shape: (3,)
col_std  = data.std(axis=0)                  # 每列的标准差，shape: (3,)
normalized = (data - col_mean) / col_std     # 广播：(3,3) - (3,) → 每行减均值再除标准差
print("归一化后每列均值：", normalized.mean(axis=0).round(10))  # 接近 0
print("归一化后每列标准差：", normalized.std(axis=0).round(10)) # 接近 1

# ══════════════════════════════════════════════════════
# 三、索引与切片
# ══════════════════════════════════════════════════════

print("\n══ 三、索引与切片 ══")

# ── 3-1 基础索引（与 Python 列表类似）────────────────

print("\n── 基础索引 ──")

arr = np.arange(10)                          # [0 1 2 3 4 5 6 7 8 9]
print("arr[3]：",   arr[3])                  # 4（第4个，0开始）
print("arr[-1]：",  arr[-1])                 # 9（最后一个）
print("arr[2:7]：", arr[2:7])               # [2 3 4 5 6]（切片，不含7）
print("arr[::2]：", arr[::2])               # [0 2 4 6 8]（步长2）
print("arr[::-1]：",arr[::-1])              # [9 8 7 6 5 4 3 2 1 0]（反转）

# 二维数组索引
m = np.array([[1,  2,  3,  4],
              [5,  6,  7,  8],
              [9, 10, 11, 12]])              # shape: (3, 4)

print("\n二维基础索引：")
print("m[1, 2]：",    m[1, 2])              # 7：第1行第2列（等同 m[1][2]）
print("m[0]：",       m[0])                 # [1 2 3 4]：第0行（整行）
print("m[:, 1]：",    m[:, 1])              # [2 6 10]：第1列（所有行的第1列）
print("m[1:3, 1:3]：",m[1:3, 1:3])         # 子矩阵，行1-2，列1-2
print("m[-1, -2:]：", m[-1, -2:])           # [11, 12]：最后一行的最后两列

# ⚠️ 视图 vs 副本：切片返回视图（共享内存），修改视图会影响原数组
view = m[0]                                  # view 与 m[0] 共享同一内存
view[0] = 999                               # 修改 view
print("\n修改 view 后 m[0]：", m[0])         # m[0] 也被改了！
m[0, 0] = 1                                 # 还原

copy = m[0].copy()                           # .copy() 显式复制，不共享内存
copy[0] = 999                               # 修改 copy
print("修改 copy 后 m[0]：", m[0])           # m[0] 不受影响

# ── 3-2 布尔索引（掩码索引）────────────────────────────

print("\n── 布尔索引 ──")

scores = np.array([88, 45, 72, 91, 55, 78, 95, 63])
names  = np.array(["小明", "小红", "小刚", "小李", "小王", "小张", "小赵", "小钱"])

# 比较运算生成布尔数组（掩码）
mask_pass = scores >= 60                     # 及格掩码，shape 与 scores 相同
print("及格掩码：", mask_pass)               # [True False True True False True True True]

# 用布尔数组作为索引，选出 True 位置的元素（返回副本，不是视图）
passing_scores = scores[mask_pass]           # 只取 True 的位置
passing_names  = names[mask_pass]            # 同一掩码应用到另一个数组
print("及格分数：", passing_scores)
print("及格姓名：", passing_names)

# 组合条件：& 表示逻辑与，| 表示逻辑或，~ 表示逻辑非（不能用 and/or/not）
# 每个条件必须用括号括起来，因为 & 优先级高于比较运算符
good = scores[(scores >= 75) & (scores < 90)]    # 75 ≤ 分数 < 90
print("良好区间：", good)                    # [88 72 78]

top_or_fail = scores[(scores >= 90) | (scores < 60)]  # 优秀或不及格
print("优秀或不及格：", top_or_fail)         # [45 91 55 95]

not_pass = scores[~mask_pass]               # ~ 取反：不及格的分数
print("不及格：", not_pass)                  # [45 55]

# np.where：根据条件选择值（向量化的三元表达式）
# np.where(条件, 条件True时取, 条件False时取)
labels = np.where(scores >= 60, "及格", "不及格")  # 每个元素独立判断
print("及格标签：", labels)

grade = np.where(scores >= 90, "优秀",
        np.where(scores >= 75, "良好",
        np.where(scores >= 60, "及格", "不及格")))  # 嵌套 where 实现多条件
print("等级：", grade)

# 布尔索引赋值：修改满足条件的元素
scores_copy = scores.copy()
scores_copy[scores_copy < 60] = 60          # 不及格的强制提到 60 分
print("补救后分数：", scores_copy)

# ── 3-3 花式索引（Fancy Indexing）────────────────────

print("\n── 花式索引 ──")

arr = np.array([10, 20, 30, 40, 50, 60, 70, 80])

# 整数数组作为索引：按指定位置取元素（可乱序、可重复）
idx = np.array([3, 0, 6, 1, 3])             # 索引数组
print("花式索引：", arr[idx])               # [40 10 70 20 40]（3号重复取了两次）

# 二维数组的花式索引
m2 = np.array([[ 1,  2,  3],
               [ 4,  5,  6],
               [ 7,  8,  9],
               [10, 11, 12]])               # shape: (4, 3)

rows = np.array([0, 2, 3])                  # 取第 0、2、3 行
print("按行花式索引:\n", m2[rows])           # 三行子矩阵

# 同时指定行和列：取散点（(0,0), (2,1), (3,2) 三个位置）
row_idx = np.array([0, 2, 3])
col_idx = np.array([0, 1, 2])
print("散点花式索引：", m2[row_idx, col_idx])  # [1, 8, 12]（对角线上的三个元素）

# np.ix_：生成开放式网格，用于取子矩阵（行×列的全组合，而非散点）
r = np.array([0, 2])                        # 取第 0 和 2 行
c = np.array([0, 2])                        # 取第 0 和 2 列
print("np.ix_ 子矩阵:\n", m2[np.ix_(r, c)]) # 2×2 子矩阵：(0,0),(0,2),(2,0),(2,2)

# 花式索引赋值
arr2 = np.zeros(8, dtype=int)
arr2[[1, 3, 5]] = [10, 30, 50]             # 把 10、30、50 分别写入索引 1、3、5
print("花式赋值：", arr2)                   # [0 10 0 30 0 50 0 0]

# ══════════════════════════════════════════════════════
# 四、常用聚合函数
# ══════════════════════════════════════════════════════

print("\n══ 四、常用聚合函数 ══")

data = np.array([[85, 92, 78, 90],           # 4名学生，4门课程的成绩
                 [72, 68, 88, 75],
                 [95, 87, 91, 89],
                 [60, 73, 65, 71]])

print("成绩矩阵:\n", data)
print(f"shape: {data.shape}")               # (4, 4)

# ── 4-1 全局聚合（不指定 axis）────────────────────────

print("\n── 全局聚合 ──")

print(f"总和  sum：   {np.sum(data)}")       # 所有元素求和
print(f"均值  mean：  {np.mean(data):.2f}") # 所有元素平均值
print(f"标准差 std：  {np.std(data):.2f}")  # 总体标准差（ddof=0，即除以 N）
print(f"方差  var：   {np.var(data):.2f}")  # 方差 = std²
print(f"最大值 max：  {np.max(data)}")       # 全局最大值
print(f"最小值 min：  {np.min(data)}")       # 全局最小值
print(f"中位数 median：{np.median(data)}")   # 中位数（排序后中间值）
print(f"极差  ptp：   {np.ptp(data)}")       # peak to peak = max - min

# ── 4-2 沿轴聚合（axis 参数）─────────────────────────

print("\n── 沿轴聚合 ──")

# axis=0：沿行方向压缩（每列聚合），结果 shape=(列数,)，即"按列统计"
# axis=1：沿列方向压缩（每行聚合），结果 shape=(行数,)，即"按行统计"

col_mean = np.mean(data, axis=0)             # 每列（每门课）的平均分
row_mean = np.mean(data, axis=1)             # 每行（每个学生）的平均分

print("每门课平均分（axis=0）：", col_mean.round(2))
print("每个学生均分（axis=1）：", row_mean.round(2))

col_std = np.std(data, axis=0)               # 每门课的标准差（分数离散程度）
print("每门课标准差：", col_std.round(2))

col_max = np.max(data, axis=0)               # 每列最高分
row_min = np.min(data, axis=1)               # 每行（每人）最低分
print("每门课最高分：", col_max)
print("每人最低分：  ", row_min)

# sum 的 axis：
print("各行总分（axis=1）：", np.sum(data, axis=1))   # 每人四科总分
print("各列总分（axis=0）：", np.sum(data, axis=0))   # 每科四人总分

# keepdims=True：保留被压缩的维度为大小1，便于广播
col_mean_kd = np.mean(data, axis=0, keepdims=True)   # shape: (1,4) 而非 (4,)
print("keepdims 后 shape：", col_mean_kd.shape)
centered = data - col_mean_kd                         # (4,4) - (1,4) 广播，按列去中心化
print("按列去中心化:\n", centered)

# ── 4-3 argmax / argmin：最值的位置 ──────────────────

print("\n── argmax / argmin ──")

scores_1d = np.array([78, 92, 85, 95, 88, 72])

max_idx = np.argmax(scores_1d)               # 返回最大值的索引（不是值本身）
min_idx = np.argmin(scores_1d)               # 返回最小值的索引

print(f"最高分索引：{max_idx}，分数：{scores_1d[max_idx]}")   # 索引3，分数95
print(f"最低分索引：{min_idx}，分数：{scores_1d[min_idx]}")   # 索引5，分数72

# 二维数组 argmax（含 axis）
max_per_row = np.argmax(data, axis=1)        # 每行最大值所在列索引（每人最高分科目）
max_per_col = np.argmax(data, axis=0)        # 每列最大值所在行索引（每科最高分学生）
print("每人最高分科目（列索引）：", max_per_row)
print("每科最高分学生（行索引）：", max_per_col)

# ── 4-4 排序相关 ──────────────────────────────────────

print("\n── 排序 ──")

arr_unsorted = np.array([3, 1, 4, 1, 5, 9, 2, 6])

sorted_arr = np.sort(arr_unsorted)           # 返回排好序的副本，原数组不变
print("sort（副本）：", sorted_arr)

arr_unsorted.sort()                          # 原地排序（修改自身），无返回值
print("sort（原地）：", arr_unsorted)

# argsort：返回"使数组有序的索引序列"（间接排序）
vals = np.array([40, 10, 30, 20, 50])
order = np.argsort(vals)                     # [1 3 2 0 4]：先取索引1(10)，再取索引3(20)...
print("argsort：", order)                    # [1 3 2 0 4]
print("按 argsort 排序：", vals[order])      # [10 20 30 40 50]

# 实用场景：按学生总分降序排名
totals = np.sum(data, axis=1)                # 每人总分
rank_idx = np.argsort(totals)[::-1]          # argsort 默认升序，[::-1] 反转得降序
student_names = np.array(["学生A", "学生B", "学生C", "学生D"])
print("\n成绩排名（降序）：")
for rank, idx in enumerate(rank_idx, start=1):
    print(f"  第{rank}名：{student_names[idx]}，总分 {totals[idx]}")

# ── 4-5 统计函数补充 ──────────────────────────────────

print("\n── 统计补充 ──")

data_1d = np.array([2, 4, 4, 6, 6, 6, 8, 10])

# 百分位数：np.percentile(arr, q)，q 是百分比（0~100）
print(f"25百分位数（Q1）：{np.percentile(data_1d, 25)}")  # 四分位数
print(f"50百分位数（中位）：{np.percentile(data_1d, 50)}")
print(f"75百分位数（Q3）：{np.percentile(data_1d, 75)}")

# np.unique：去重并返回唯一值（已排序）
arr_dup = np.array([3, 1, 2, 3, 1, 4, 2])
unique_vals, counts = np.unique(arr_dup, return_counts=True)  # return_counts 同时返回频次
print(f"唯一值：{unique_vals}")              # [1 2 3 4]
print(f"出现次数：{counts}")                 # [2 2 2 1]

# np.cumsum / np.cumprod：累积求和 / 累积乘积
print(f"累积求和：{np.cumsum(np.array([1,2,3,4,5]))}")   # [ 1  3  6 10 15]
print(f"累积乘积：{np.cumprod(np.array([1,2,3,4,5]))}")  # [  1  2  6 24 120]

# np.diff：相邻元素差（金融中常用于计算价格变动）
prices = np.array([100, 105, 103, 108, 106])
print(f"每日涨跌：{np.diff(prices)}")        # [5 -2  5 -2]（正数涨，负数跌）

# np.clip：将数组元素限制在 [min, max] 范围内（截断）
raw = np.array([-5, 0, 3, 8, 15, -2])
clipped = np.clip(raw, a_min=0, a_max=10)    # 小于0变0，大于10变10
print(f"clip(0,10)：{clipped}")              # [0 0 3 8 10 0]

# ══════════════════════════════════════════════════════
# 五、综合示例：学生成绩分析
# ══════════════════════════════════════════════════════

print("\n══ 五、综合示例：成绩分析 ══")

rng2 = np.random.default_rng(seed=0)

# 模拟 30 名学生、5 门课的成绩（正态分布，均值75，标准差12，截断到[0,100]）
n_students = 30
n_subjects  = 5
raw_scores  = rng2.normal(loc=75, scale=12, size=(n_students, n_subjects))
scores_mat  = np.clip(raw_scores, 0, 100).round(1)   # 截断并保留1位小数

subjects = ["语文", "数学", "英语", "物理", "化学"]

# ── 学生维度统计（axis=1：按行聚合）──────────────────
student_total  = np.sum(scores_mat,  axis=1)          # 每人总分
student_avg    = np.mean(scores_mat, axis=1).round(1) # 每人均分
student_rank   = np.argsort(student_total)[::-1]      # 按总分降序排名

print("前5名学生：")
print(f"  {'排名':^4} {'学号':^6} {'总分':>6} {'均分':>6}")
print("  " + "-" * 26)
for rank, idx in enumerate(student_rank[:5], 1):
    print(f"  {rank:^4} {'S'+str(idx+1):^6} {student_total[idx]:>6.1f} {student_avg[idx]:>6.1f}")

# ── 科目维度统计（axis=0：按列聚合）──────────────────
subj_mean = np.mean(scores_mat, axis=0).round(1)      # 每科平均分
subj_std  = np.std(scores_mat,  axis=0).round(1)      # 每科标准差（分数离散程度）
subj_pass = np.sum(scores_mat >= 60, axis=0)           # 每科及格人数

print("\n各科目统计：")
print(f"  {'科目':^4} {'平均分':>6} {'标准差':>6} {'及格人数':>8}")
print("  " + "-" * 30)
for i, subj in enumerate(subjects):
    print(f"  {subj:^4} {subj_mean[i]:>6.1f} {subj_std[i]:>6.1f} {subj_pass[i]:>8}")

# ── 全局统计 ──────────────────────────────────────────
overall_pass_rate = np.mean(scores_mat >= 60) * 100    # 所有科目总及格率
high_score_count  = np.sum(scores_mat >= 90)           # 全部优秀（90+）次数
below_avg_mask    = student_avg < np.mean(student_avg) # 低于班级均分的学生掩码

print(f"\n全局统计：")
print(f"  总体及格率：{overall_pass_rate:.1f}%")
print(f"  优秀（≥90）次数：{high_score_count}")
print(f"  低于班级均分的学生数：{np.sum(below_avg_mask)}")
print(f"  全班最高单科分：{np.max(scores_mat)}")
print(f"  全班最低单科分：{np.min(scores_mat)}")

# ── 标准化分数（Z-score）：消除科目难度差异 ───────────
z_scores = (scores_mat - subj_mean) / subj_std         # 广播：(30,5) - (5,) / (5,)
print(f"\nZ-score 统计验证：")
print(f"  各科均值（应≈0）：{np.mean(z_scores, axis=0).round(3)}")
print(f"  各科标准差（应≈1）：{np.std(z_scores, axis=0).round(3)}")

# 综合 Z-score 排名（各科 Z-score 之和越大，说明该生相对表现越好）
z_total = np.sum(z_scores, axis=1)
z_rank  = np.argsort(z_total)[::-1]
print(f"\n按 Z-score 综合排名前3：")
for rank, idx in enumerate(z_rank[:3], 1):
    print(f"  第{rank}名：S{idx+1}，Z-score总分 {z_total[idx]:.3f}，原始均分 {student_avg[idx]}")
