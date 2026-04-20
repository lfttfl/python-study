# Python 数据分析练习：Pandas 基础
# =====================================================

import pandas as pd                           # Pandas 是表格数据处理的核心库，惯例别名 pd
import numpy as np                            # 配合 NumPy 使用
import os
from pathlib import Path

print(f"Pandas 版本：{pd.__version__}")

WORK_DIR = Path(__file__).parent / "tmp_pandas"   # 存放练习生成的临时文件
WORK_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════
# 一、Series：一维带标签数组
# ══════════════════════════════════════════════════════

print("\n══ 一、Series ══")

# Series 是 Pandas 的一维数据结构，相当于"带行标签的一列"
# 每个元素都有对应的索引（index），默认是 0, 1, 2, ...（可自定义为任意值）

# ── 1-1 创建 Series ──────────────────────────────────

# 从列表创建（默认整数索引）
s1 = pd.Series([10, 20, 30, 40, 50])         # 自动生成 RangeIndex(0, 5)
print("列表创建 Series：")
print(s1)
print(f"dtype：{s1.dtype}，shape：{s1.shape}，size：{s1.size}")

# 从列表 + 自定义索引
s2 = pd.Series(
    [88, 92, 75, 91],
    index=["语文", "数学", "英语", "物理"],   # index 可以是任意可哈希类型
    name="小明的成绩",                         # name 属性，作为列名时很重要
)
print("\n带标签 Series：")
print(s2)

# 从字典创建（键自动成为索引）
scores_dict = {"小明": 88, "小红": 92, "小刚": 75, "小李": 91}
s3 = pd.Series(scores_dict, name="班级成绩")  # 字典的键变成 index，值变成 data
print("\n字典创建 Series：")
print(s3)

# 标量广播：单个值填充到所有索引
s4 = pd.Series(100, index=["a", "b", "c", "d"])  # 所有行都是 100
print("\n标量广播：", s4.tolist())

# 从 NumPy 数组创建
arr = np.linspace(0, 1, 5)
s5 = pd.Series(arr, index=[f"x{i}" for i in range(5)])  # 列表推导式生成标签
print("\nNumPy 数组创建：")
print(s5.round(3))

# ── 1-2 Series 基本属性与操作 ─────────────────────────

print("\n── Series 属性与操作 ──")

s = pd.Series([88, 92, 75, 91, 68, 85],
              index=["小明", "小红", "小刚", "小李", "小王", "小张"],
              name="期末成绩")

print(f"index：{s.index.tolist()}")           # 索引列表
print(f"values（ndarray）：{s.values}")       # 底层 NumPy 数组
print(f"dtype：{s.dtype}")                   # 数据类型
print(f"name：{s.name}")                     # Series 名称

# 索引访问：方括号 + 标签
print(f"\ns['小明']：{s['小明']}")            # 88，按标签取值
print(f"s[0]：{s.iloc[0]}")                  # 88，按位置取值（用 iloc 更安全）
print(f"s[['小明','小红']]：\n{s[['小明','小红']]}")  # 多标签取子集

# 向量化运算（与 NumPy 一致）
print("\n加 5 分：")
print(s + 5)                                  # 每个元素加 5，保留原索引

# 布尔筛选
print("\n及格（>=60）：")
print(s[s >= 60])                             # 布尔索引，只保留 True 的行

# 常用统计方法
print(f"\n均值：{s.mean():.2f}")
print(f"中位数：{s.median():.1f}")
print(f"标准差：{s.std():.2f}")
print(f"最大值：{s.max()}（{s.idxmax()}）")  # idxmax() 返回最大值的索引标签
print(f"最小值：{s.min()}（{s.idxmin()}）")
print(f"排名（升序）：\n{s.rank()}")          # 返回每个值的排名（1 = 最小）

# value_counts()：统计每个值出现次数（常用于分类数据）
grades = pd.Series(["优秀","良好","及格","良好","优秀","优秀","不及格","及格"])
print("\nvalue_counts()：")
print(grades.value_counts())                  # 按频次降序排列

# apply()：对每个元素应用函数
grade_series = s.apply(lambda x: "优秀" if x >= 90 else "良好" if x >= 75 else "及格")
print("\napply 等级：")
print(grade_series)

# ── 1-3 Series 对齐（自动按索引对齐）────────────────

print("\n── Series 对齐 ──")

# Pandas 的核心特性：两个 Series 运算时自动按索引对齐，缺失则为 NaN
s_a = pd.Series({"小明": 88, "小红": 92, "小刚": 75})
s_b = pd.Series({"小明": 10, "小红":  5, "小王": 20})   # 小王在 s_a 中没有

result = s_a + s_b                            # 索引对齐后相加，缺失的变成 NaN
print("s_a + s_b（含对齐）：")
print(result)                                 # 小刚和小王都是 NaN（一方缺失）

# fill_value 参数：缺失时用指定值填充（而非 NaN）
result2 = s_a.add(s_b, fill_value=0)         # 缺失的那方视为 0
print("\nadd(fill_value=0)：")
print(result2)                                # 小刚=75+0=75，小王=0+20=20

# ══════════════════════════════════════════════════════
# 二、DataFrame：二维表格数据结构
# ══════════════════════════════════════════════════════

print("\n══ 二、DataFrame ══")

# DataFrame 是 Pandas 最核心的数据结构，类似电子表格/数据库表
# 由多列组成，每列是一个 Series，所有列共享同一个行索引（index）

# ── 2-1 创建 DataFrame ───────────────────────────────

# 从字典创建（最常用）：键是列名，值是列表（各列等长）
df = pd.DataFrame({
    "姓名":  ["小明", "小红", "小刚", "小李", "小王", "小张"],
    "年龄":  [18, 17, 19, 18, 20, 17],
    "城市":  ["北京", "上海", "北京", "广州", "深圳", "上海"],
    "语文":  [85, 92, 72, 88, 65, 90],
    "数学":  [90, 88, 78, 95, 72, 85],
    "英语":  [78, 95, 68, 82, 80, 91],
})
print("基础 DataFrame：")
print(df)
print(f"\nshape：{df.shape}")                 # (6, 6)：6行6列
print(f"行数：{len(df)}")                     # 等于 df.shape[0]

# 从列表的列表创建（配合 columns 参数）
data_list = [[1, "Alice", 90.5],
             [2, "Bob",   85.0],
             [3, "Carol", 92.3]]
df2 = pd.DataFrame(data_list, columns=["id", "name", "score"])
print("\n列表创建 DataFrame：")
print(df2)

# 从字典列表创建（每个字典是一行）
records = [
    {"product": "苹果", "price": 5.5,  "stock": 100},
    {"product": "香蕉", "price": 3.2,  "stock": 200},
    {"product": "橙子", "price": 4.8,  "stock": 150},
]
df3 = pd.DataFrame(records)                   # 字典的键自动成为列名
print("\n字典列表创建：")
print(df3)

# 从 NumPy 数组创建
arr = np.arange(1, 13).reshape(3, 4)
df4 = pd.DataFrame(arr, columns=["A", "B", "C", "D"],
                   index=["行1", "行2", "行3"])  # 自定义行索引
print("\nNumPy 数组创建：")
print(df4)

# ── 2-2 DataFrame 基本属性 ───────────────────────────

print("\n── DataFrame 属性 ──")

print(f"columns：{df.columns.tolist()}")      # 列名列表
print(f"index：{df.index.tolist()}")          # 行索引列表（默认是 RangeIndex）
print(f"dtypes：\n{df.dtypes}")               # 每列的数据类型
print(f"values（ndarray）：\n{df.values}")    # 底层二维 NumPy 数组（所有列同类型时高效）

# ── 2-3 列操作 ───────────────────────────────────────

print("\n── 列操作 ──")

# 取单列：返回 Series
print("取'姓名'列（Series）：")
print(df["姓名"])                             # df["列名"] 是标准写法
print(df.姓名)                               # df.列名 也可以，但列名含空格/与方法同名时不行

# 取多列：返回 DataFrame（传入列名列表）
print("\n取语数英三列（DataFrame）：")
print(df[["语文", "数学", "英语"]])

# 新增列：直接赋值
df["总分"] = df["语文"] + df["数学"] + df["英语"]   # 逐行求和
df["均分"] = df["总分"] / 3                          # 除以科目数
print("\n新增总分和均分后：")
print(df)

# 修改列（用 assign 返回新 DataFrame，不改原始数据）
df_rounded = df.assign(均分=df["均分"].round(1))     # assign 返回副本
print("\nassign 四舍五入均分（不改原 df）：")
print(df_rounded[["姓名", "均分"]])

# 删除列
df_dropped = df.drop(columns=["总分", "均分"])       # drop 返回副本，原 df 不变
print("\ndrop 后的列：", df_dropped.columns.tolist())
df.drop(columns=["均分"], inplace=True)              # inplace=True 直接修改原 df

# 列重命名
df_renamed = df.rename(columns={"语文": "Chinese", "数学": "Math"})
print("\n重命名后的列：", df_renamed.columns.tolist())

# ══════════════════════════════════════════════════════
# 三、数据查看
# ══════════════════════════════════════════════════════

print("\n══ 三、数据查看 ══")

# 生成一个更大的练习 DataFrame
np.random.seed(42)
n = 20
df_large = pd.DataFrame({
    "学号":   [f"S{i:03d}" for i in range(1, n+1)],   # S001 ~ S020
    "姓名":   [f"学生{i}"  for i in range(1, n+1)],
    "年龄":   np.random.randint(17, 21, n),
    "班级":   np.random.choice(["A班", "B班", "C班"], n),
    "语文":   np.random.randint(60, 100, n),
    "数学":   np.random.randint(55, 100, n),
    "英语":   np.random.randint(60, 100, n),
    "体育":   np.random.randint(70, 100, n),
})
df_large["总分"] = df_large[["语文","数学","英语","体育"]].sum(axis=1)   # 行方向求和

# ── 3-1 head / tail：查看前 N 行 / 后 N 行 ──────────

print("── head / tail ──")
print("前 3 行：")
print(df_large.head(3))                       # 默认 head(5)，这里取 3 行
print("\n后 3 行：")
print(df_large.tail(3))                       # 默认 tail(5)

# ── 3-2 shape / len / size ───────────────────────────

print("\n── shape / len ──")
print(f"shape：{df_large.shape}")             # (20, 9)：行数×列数
print(f"行数 len：{len(df_large)}")            # 20：等同 shape[0]
print(f"元素总数 size：{df_large.size}")       # 20×9=180

# ── 3-3 info()：数据类型与缺失值概览 ─────────────────

print("\n── info() ──")
df_large.info()                               # 输出：列名、非空数量、dtype，非常实用

# ── 3-4 describe()：数值列的统计摘要 ─────────────────

print("\n── describe() ──")
print(df_large.describe().round(2))           # count/mean/std/min/25%/50%/75%/max

# describe(include="object")：对字符串列统计（count/unique/top/freq）
print("\ndescribe(字符串列)：")
print(df_large.describe(include="object"))

# ── 3-5 nunique / value_counts ───────────────────────

print("\n── nunique / value_counts ──")
print("各列唯一值数量：")
print(df_large.nunique())                     # 每列有多少个不同的值

print("\n班级分布：")
print(df_large["班级"].value_counts())        # 每个班有多少学生

print("\n班级分布（比例）：")
print(df_large["班级"].value_counts(normalize=True).round(3))  # normalize=True 转为占比

# ══════════════════════════════════════════════════════
# 四、数据读取与写入
# ══════════════════════════════════════════════════════

print("\n══ 四、数据读取与写入 ══")

# ── 4-1 写入并读取 CSV ───────────────────────────────

csv_path = WORK_DIR / "students.csv"
df_large.to_csv(csv_path,                    # 写入 CSV
                index=False,                  # index=False：不把行索引写入文件
                encoding="utf-8-sig")         # utf-8-sig：Windows Excel 打开不乱码

print(f"CSV 写入：{csv_path.name}（{csv_path.stat().st_size} 字节）")

# read_csv：参数众多，以下是最常用的
df_from_csv = pd.read_csv(
    csv_path,
    encoding="utf-8-sig",                    # 与写入编码一致
    # header=0,                              # 第 0 行为表头（默认），header=None 无表头
    # index_col=0,                           # 用第 0 列作行索引（当时 index=True 写入时用）
    # usecols=["姓名","语文","数学"],         # 只读取指定列，节省内存
    # nrows=10,                              # 只读取前 10 行（大文件预览用）
    # dtype={"年龄": np.int32},              # 指定列的类型
    # na_values=["N/A", "缺失", "-"],        # 自定义缺失值标记
)
print(f"CSV 读回：{df_from_csv.shape} 行列，列：{df_from_csv.columns.tolist()}")

# 读取 CSV 时的分块（大文件）
chunk_iter = pd.read_csv(csv_path, encoding="utf-8-sig", chunksize=5)  # 每次 5 行
chunks = [chunk for chunk in chunk_iter]     # 收集所有块
print(f"分块读取：{len(chunks)} 块，总行数 = {sum(len(c) for c in chunks)}")

# ── 4-2 写入并读取 Excel ─────────────────────────────

excel_path = WORK_DIR / "students.xlsx"

# to_excel：需要 openpyxl 库
df_large.to_excel(
    excel_path,
    sheet_name="学生成绩",                   # 工作表名称
    index=False,                              # 不写行索引
    engine="openpyxl",                        # 指定引擎（默认也是 openpyxl）
)
print(f"\nExcel 写入：{excel_path.name}（{excel_path.stat().st_size} 字节）")

# read_excel：读取 Excel 文件
df_from_excel = pd.read_excel(
    excel_path,
    sheet_name="学生成绩",                   # 指定工作表名（也可用整数索引 0）
    engine="openpyxl",
)
print(f"Excel 读回：{df_from_excel.shape}")

# ExcelWriter：把多个 DataFrame 写入同一个 Excel 文件的不同工作表
multi_excel = WORK_DIR / "multi_sheet.xlsx"
with pd.ExcelWriter(multi_excel, engine="openpyxl") as writer:    # 上下文管理器
    df_large[df_large["班级"]=="A班"].to_excel(writer, sheet_name="A班", index=False)
    df_large[df_large["班级"]=="B班"].to_excel(writer, sheet_name="B班", index=False)
    df_large[df_large["班级"]=="C班"].to_excel(writer, sheet_name="C班", index=False)
print(f"多工作表 Excel：{multi_excel.name}")

# ── 4-3 to_dict / from_dict：与字典互转 ──────────────

print("\n── DataFrame ↔ 字典 ──")

small_df = df_large.head(3)[["姓名","语文","数学"]]

# orient 参数控制转换方向
d_records = small_df.to_dict(orient="records")   # 列表，每个元素是一行的字典
d_dict    = small_df.to_dict(orient="dict")      # 嵌套字典：{列名: {行索引: 值}}
d_list    = small_df.to_dict(orient="list")      # 字典：{列名: [值列表]}

print("records 格式：", d_records)
print("list 格式：",    d_list)

# 从字典恢复 DataFrame
df_back = pd.DataFrame.from_records(d_records)
print("从 records 恢复：\n", df_back)

# ══════════════════════════════════════════════════════
# 五、索引操作：loc、iloc、条件筛选
# ══════════════════════════════════════════════════════

print("\n══ 五、索引操作 ══")

# 重置索引以便演示（把学号设为行索引）
df_idx = df_large.set_index("学号")          # set_index：指定某列为行索引
print("以学号为索引（前3行）：")
print(df_idx.head(3))

# ── 5-1 loc：按标签（索引名、列名）索引 ──────────────

print("\n── loc（标签索引）──")

# loc[行标签, 列标签]：两个维度都用标签
print("单行单列 loc['S001', '语文']：", df_idx.loc["S001", "语文"])

print("\n单行多列：")
print(df_idx.loc["S001", ["姓名", "语文", "数学"]])  # 选一行的指定列

print("\n多行单列（切片标签，包含终点！）：")
print(df_idx.loc["S001":"S005", "语文"])     # loc 切片含两端，与 Python 切片不同

print("\n多行多列：")
print(df_idx.loc["S001":"S004", "语文":"英语"])  # 行标签切片 × 列标签切片

print("\n所有行的指定列（: 表示全部行）：")
print(df_idx.loc[:, ["姓名", "总分"]].head(4))

# ── 5-2 iloc：按整数位置索引（position-based）────────

print("\n── iloc（位置索引）──")

# iloc[行位置, 列位置]：纯整数，与列名/索引无关，与 NumPy 切片完全一致
print("iloc[0, 0]：", df_idx.iloc[0, 0])     # 第0行第0列的值

print("\nioc[0:3, 0:3]：")                   # iloc 切片不含右端（与 Python 切片一致）
print(df_idx.iloc[0:3, 0:3])

print("\nioc[[0, 2, 4], -1]（花式+负索引）：")
print(df_idx.iloc[[0, 2, 4], -1])            # 第0、2、4行的最后一列（-1）

print("\nioc[::3, :] 每隔3行：")
print(df_idx.iloc[::3, :].head())            # 每隔3行取一行（步长=3）

# loc vs iloc 区别总结：
# loc  → 标签；切片含终点；列名要写字符串
# iloc → 整数位置；切片不含终点；只写数字

# ── 5-3 at / iat：单值快速访问 ───────────────────────

print("\n── at / iat ──")

# at[行标签, 列标签]：比 loc 更快，只用于访问单个标量值
print("at['S003', '数学']：", df_idx.at["S003", "数学"])

# iat[行位置, 列位置]：比 iloc 更快，只用于单个标量值
print("iat[2, 3]：",          df_idx.iat[2, 3])   # 第2行第3列

# 赋值：at/iat 也支持写入
df_idx.at["S001", "语文"] = 99               # 修改单个值

# ── 5-4 条件筛选 ─────────────────────────────────────

print("\n── 条件筛选 ──")

# 单条件：语文 >= 85
high_chinese = df_large[df_large["语文"] >= 85]
print(f"语文≥85的学生（{len(high_chinese)}人）：")
print(high_chinese[["姓名","班级","语文"]].to_string(index=False))

# 多条件（& 且，| 或，~ 非）
# 每个条件必须用括号括起来！
mask = (df_large["语文"] >= 85) & (df_large["数学"] >= 85)
both_good = df_large[mask]
print(f"\n语文数学都≥85的（{len(both_good)}人）：")
print(both_good[["姓名","语文","数学"]])

# isin()：检查值是否在给定列表中（代替多个 == 的 or 连接）
bj_sh = df_large[df_large["班级"].isin(["A班", "B班"])]
print(f"\nA班或B班（{len(bj_sh)}人）：", bj_sh["班级"].value_counts().to_dict())

# between()：检查值是否在区间内（含两端）
mid_range = df_large[df_large["总分"].between(300, 350)]
print(f"\n总分300~350之间（{len(mid_range)}人）：")
print(mid_range[["姓名","总分"]])

# str 访问器：对字符串列进行向量化字符串操作
# str.contains()：包含子字符串（支持正则）
name_match = df_large[df_large["姓名"].str.contains("1|2|3")]  # 姓名含1/2/3的
print(f"\n姓名含'1'或'2'或'3'的：{name_match['姓名'].tolist()}")

# query()：用字符串表达式筛选（代码更简洁，适合多条件）
result_q = df_large.query("语文 >= 85 and 数学 >= 85")
print(f"\nquery 语文数学都≥85：{result_q['姓名'].tolist()}")

# where()：保留满足条件的行，不满足的替换为 NaN（保持形状不变）
df_where = df_large[["姓名","语文"]].where(df_large["语文"] >= 80)
print("\nwhere(语文>=80)（不满足的变NaN）：")
print(df_where.head(6))

# ══════════════════════════════════════════════════════
# 六、缺失值处理
# ══════════════════════════════════════════════════════

print("\n══ 六、缺失值处理 ══")

# 构造含缺失值的 DataFrame（NaN = Not a Number，Pandas 用 float 的 NaN 表示缺失）
df_missing = pd.DataFrame({
    "姓名":  ["小明", "小红", "小刚", "小李", "小王", "小张"],
    "年龄":  [18,   None,   19,   18,   None,   17],    # None 会被转为 NaN
    "语文":  [85.0, 92.0,  np.nan, 88.0, 65.0, 90.0],  # np.nan 就是 NaN
    "数学":  [90.0, np.nan, 78.0, np.nan, 72.0, 85.0],
    "英语":  [78.0, 95.0,  68.0, 82.0, np.nan, np.nan],
    "城市":  ["北京", "上海", None, "广州", "深圳", "上海"],
})
print("含缺失值的 DataFrame：")
print(df_missing)

# ── 6-1 检测缺失值 ───────────────────────────────────

print("\n── 检测缺失值 ──")

# isnull()：逐元素检测，缺失返回 True；notnull() 是其反义
print("isnull()：")
print(df_missing.isnull())                    # 布尔 DataFrame，True 表示缺失

# 每列缺失数量
print("\n各列缺失数量：")
print(df_missing.isnull().sum())              # axis=0（默认），每列求和

# 每列缺失比例
print("\n各列缺失比例：")
print((df_missing.isnull().mean() * 100).round(1).astype(str) + "%")

# 含有缺失值的行（任一列缺失）
any_null_rows = df_missing[df_missing.isnull().any(axis=1)]   # axis=1：行方向，任一为真
print(f"\n含缺失值的行（{len(any_null_rows)}行）：")
print(any_null_rows)

# 所有列都有缺失值的行（all：全部为真）
all_null_rows = df_missing[df_missing.isnull().all(axis=1)]
print(f"\n所有列都缺失的行：{len(all_null_rows)} 行")

# ── 6-2 dropna：删除缺失值 ───────────────────────────

print("\n── dropna ──")

# dropna()：默认删除含有任意 NaN 的行（axis=0，how='any'）
df_drop_any = df_missing.dropna()             # 删完后只剩完全没缺失的行
print(f"dropna() 后剩 {len(df_drop_any)} 行：")
print(df_drop_any)

# how='all'：只删除所有值都是 NaN 的行（更宽松）
df_drop_all = df_missing.dropna(how="all")
print(f"\ndropna(how='all') 后：{len(df_drop_all)} 行（本例无全空行，无变化）")

# subset：只在指定列检查缺失值
df_drop_sub = df_missing.dropna(subset=["语文", "数学"])   # 语文和数学都有值才保留
print(f"\ndropna(subset=['语文','数学']) 后：{len(df_drop_sub)} 行")
print(df_drop_sub)

# thresh=N：保留至少有 N 个非空值的行
df_thresh = df_missing.dropna(thresh=5)       # 至少 5 个非空值（共 6 列）
print(f"\ndropna(thresh=5) 后：{len(df_thresh)} 行")
print(df_thresh)

# axis=1：删除含缺失值的列（用得少，会丢失整列数据）
df_drop_col = df_missing.dropna(axis=1)
print(f"\ndropna(axis=1)后剩列：{df_drop_col.columns.tolist()}")

# ── 6-3 fillna：填充缺失值 ───────────────────────────

print("\n── fillna ──")

# 用固定值填充（所有 NaN 填同一个值）
df_fill_zero = df_missing.fillna(0)
print("fillna(0)：")
print(df_fill_zero)

# 用字典按列指定填充值
fill_dict = {
    "年龄": df_missing["年龄"].mean(),        # 年龄用均值填充
    "语文": df_missing["语文"].median(),       # 语文用中位数
    "数学": df_missing["数学"].mean(),
    "英语": df_missing["英语"].mean(),
    "城市": "未知",                            # 城市用固定字符串填充
}
df_fill_smart = df_missing.fillna(fill_dict)
print("\n按列智能填充：")
print(df_fill_smart.round(1))

# method（前向/后向填充，适合时间序列）
ts_data = pd.Series([1.0, np.nan, np.nan, 4.0, np.nan, 6.0])
print(f"\n时间序列：{ts_data.tolist()}")
print(f"前向填充 ffill：{ts_data.ffill().tolist()}")   # 用前一个有效值填充（forward fill）
print(f"后向填充 bfill：{ts_data.bfill().tolist()}")   # 用后一个有效值填充（backward fill）

# 对 DataFrame 也适用
df_ffill = df_missing[["语文","数学","英语"]].ffill()   # 每列独立向前填充
print("\nffill 填充：")
print(df_ffill)

# interpolate()：线性插值（数值列，比 ffill/bfill 更合理）
s_interp = pd.Series([1.0, np.nan, np.nan, 7.0, np.nan, 10.0])
print(f"\n线性插值前：{s_interp.tolist()}")
print(f"interpolate：{s_interp.interpolate().tolist()}")  # 缺失值按线性比例插入

# ── 6-4 综合缺失值处理策略 ────────────────────────────

print("\n── 综合处理策略 ──")

def clean_dataframe(df):
    """完整的缺失值处理流程"""
    print(f"  清洗前：{df.shape}，总缺失 {df.isnull().sum().sum()} 处")

    # 第一步：删除全空行
    df = df.dropna(how="all")

    # 第二步：数值列用各自中位数填充（对异常值不敏感）
    num_cols = df.select_dtypes(include="number").columns    # 自动筛选数值列
    for col in num_cols:
        median = df[col].median()
        df[col] = df[col].fillna(median)

    # 第三步：字符串列用众数（最频繁值）填充
    str_cols = df.select_dtypes(include="object").columns    # 自动筛选字符串列
    for col in str_cols:
        if df[col].isnull().any():                           # 有缺失才处理
            mode_val = df[col].mode()                        # mode() 返回 Series（可能多众数）
            df[col] = df[col].fillna(mode_val[0] if len(mode_val) > 0 else "未知")

    print(f"  清洗后：{df.shape}，总缺失 {df.isnull().sum().sum()} 处")
    return df

df_cleaned = clean_dataframe(df_missing.copy())  # 传入副本，保护原数据
print("清洗结果：")
print(df_cleaned)

# ══════════════════════════════════════════════════════
# 七、综合实战：从 CSV 加载、清洗、分析、输出
# ══════════════════════════════════════════════════════

print("\n══ 七、综合实战 ══")

# 生成含缺失值和异常值的模拟数据
np.random.seed(7)
n = 30
dirty_data = pd.DataFrame({
    "学号":  [f"S{i:03d}" for i in range(1, n+1)],
    "姓名":  [f"学生{i}"  for i in range(1, n+1)],
    "班级":  np.random.choice(["A班","B班","C班"], n),
    "语文":  np.random.randint(50, 101, n).astype(float),
    "数学":  np.random.randint(45, 101, n).astype(float),
    "英语":  np.random.randint(55, 101, n).astype(float),
    "体育":  np.random.randint(60, 101, n).astype(float),
})

# 随机插入 NaN
for col in ["语文","数学","英语","体育"]:
    idx = np.random.choice(n, size=3, replace=False)  # 随机选3行
    dirty_data.loc[idx, col] = np.nan                  # 设为 NaN

dirty_csv = WORK_DIR / "dirty_students.csv"
dirty_data.to_csv(dirty_csv, index=False, encoding="utf-8-sig")

# ── Step 1：读取 ──────────────────────────────────────
df_raw = pd.read_csv(dirty_csv, encoding="utf-8-sig")
print(f"原始数据：{df_raw.shape}，缺失值：\n{df_raw.isnull().sum()}")

# ── Step 2：清洗 ──────────────────────────────────────
df_clean = df_raw.copy()
score_cols = ["语文", "数学", "英语", "体育"]

for col in score_cols:
    col_median = df_clean[col].median()       # 用中位数填充，受异常值影响小
    df_clean[col] = df_clean[col].fillna(col_median)
    df_clean[col] = df_clean[col].round(1)   # 保留1位小数（中位数可能是整数或.5）

print(f"\n清洗后缺失值：{df_clean.isnull().sum().sum()}")

# ── Step 3：特征工程 ──────────────────────────────────
df_clean["总分"]  = df_clean[score_cols].sum(axis=1)
df_clean["均分"]  = df_clean[score_cols].mean(axis=1).round(1)
df_clean["等级"]  = pd.cut(                  # pd.cut：将连续值分箱（离散化）
    df_clean["均分"],
    bins=[0, 60, 75, 90, 100],               # 分箱边界
    labels=["不及格", "及格", "良好", "优秀"],  # 每个区间的标签
    right=True,                              # 右端点包含（默认）
)
df_clean["排名"]  = df_clean["总分"].rank(ascending=False, method="min").astype(int)

# ── Step 4：班级维度分析 ──────────────────────────────
print("\n── 各班成绩汇总 ──")
summary = df_clean.groupby("班级")[score_cols + ["总分"]].agg(
    ["mean", "max", "min"]                   # 同时计算三个聚合函数
).round(1)
print(summary)

# ── Step 5：筛选与输出 ────────────────────────────────
print("\n── Top 5 学生 ──")
top5 = (df_clean
        .sort_values("总分", ascending=False)   # 按总分降序排
        .head(5)
        [["学号","姓名","班级","总分","均分","等级","排名"]])
print(top5.to_string(index=False))

# ── Step 6：保存结果 ──────────────────────────────────
result_path = WORK_DIR / "analysis_result.csv"
df_clean.to_csv(result_path, index=False, encoding="utf-8-sig")
print(f"\n分析结果已保存：{result_path.name}（{result_path.stat().st_size} 字节）")

# ── 清理临时文件 ──────────────────────────────────────
import shutil
print(f"\n共生成文件：{[f.name for f in WORK_DIR.iterdir()]}")
shutil.rmtree(WORK_DIR)
print(f"已清理临时目录：{WORK_DIR.name}/")
