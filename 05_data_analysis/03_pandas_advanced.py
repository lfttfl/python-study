# Python 数据分析练习：Pandas 进阶
# =====================================================

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")             # 屏蔽 pandas 版本迁移警告，保持输出整洁

print(f"Pandas 版本：{pd.__version__}")

WORK_DIR = Path(__file__).parent / "tmp_adv"
WORK_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════
# 一、数据清洗：重复值与异常值
# ══════════════════════════════════════════════════════

print("\n══ 一、数据清洗 ══")

# ── 1-1 构造含脏数据的 DataFrame ──────────────────────

df_dirty = pd.DataFrame({
    "订单ID": ["O001","O002","O003","O002","O004","O005","O003","O006"],  # O002/O003 重复
    "客户":   ["小明","小红","小刚","小红","小李","小王","小刚","小张"],
    "产品":   ["苹果","香蕉","苹果","香蕉","橙子","苹果","苹果","葡萄"],
    "数量":   [10, 5, 8, 5, -3, 1000, 8, 6],   # -3 是负数异常值，1000 是极端异常值
    "单价":   [5.5, 3.2, 5.5, 3.2, 4.8, 5.5, 5.5, 12.0],
    "城市":   ["北京","上海","北京","上海","广州","深圳","北京","成都"],
})
df_dirty["金额"] = df_dirty["数量"] * df_dirty["单价"]   # 计算金额（含异常值）
print("原始脏数据：")
print(df_dirty)

# ── 1-2 重复值检测与处理 ──────────────────────────────

print("\n── 重复值处理 ──")

# duplicated()：逐行检测是否重复，返回布尔 Series
# keep='first'（默认）：第一次出现标记为 False，后续重复标记为 True
# keep='last'：最后一次出现标记为 False，其余标记为 True
# keep=False：所有重复行都标记为 True
dup_mask = df_dirty.duplicated()              # 默认按所有列判断是否完全重复
print(f"完全重复行数：{dup_mask.sum()}")      # 本例有 2 行完全重复（O002/O003 各出现两次）
print("重复行内容：")
print(df_dirty[dup_mask])                     # 显示重复行

# 按指定列判断重复（只要订单ID相同就视为重复）
dup_by_id = df_dirty.duplicated(subset=["订单ID"], keep="first")
print(f"\n按订单ID重复行数：{dup_by_id.sum()}")
print(df_dirty[dup_by_id])

# drop_duplicates()：删除重复行，返回新 DataFrame（原数据不变）
df_no_dup = df_dirty.drop_duplicates(subset=["订单ID"], keep="first")  # 保留首次出现
print(f"\n去重后：{len(df_no_dup)} 行（原 {len(df_dirty)} 行）")
print(df_no_dup.reset_index(drop=True))       # reset_index 重置行号，drop=True 丢掉旧索引

# ── 1-3 异常值检测与处理 ──────────────────────────────

print("\n── 异常值处理 ──")

df_clean = df_no_dup.copy()                   # 从去重后的数据继续处理
df_clean = df_clean.reset_index(drop=True)    # 重置索引，方便后续操作

# 方法1：业务规则（最直观）——数量必须 > 0 且 <= 合理上限
valid_qty = df_clean["数量"].between(1, 500)  # between 含两端，定义合法范围
print("数量异常行：")
print(df_clean[~valid_qty][["订单ID","数量","金额"]])   # ~ 取反：异常的行

df_clean = df_clean[valid_qty].reset_index(drop=True)   # 只保留合法行
print(f"业务规则过滤后：{len(df_clean)} 行")

# 方法2：IQR（四分位距）——统计方法检测离群点
nums = pd.Series([2, 4, 5, 6, 5, 4, 3, 100, 5, 4])    # 100 是离群点

Q1  = nums.quantile(0.25)                     # 第25百分位数（下四分位数）
Q3  = nums.quantile(0.75)                     # 第75百分位数（上四分位数）
IQR = Q3 - Q1                                 # 四分位距
lower = Q1 - 1.5 * IQR                        # 下界：Q1 - 1.5×IQR（统计学惯例）
upper = Q3 + 1.5 * IQR                        # 上界：Q3 + 1.5×IQR
outliers = nums[(nums < lower) | (nums > upper)]
print(f"\nIQR 方法：Q1={Q1} Q3={Q3} IQR={IQR} 下界={lower} 上界={upper}")
print(f"检测到离群点：{outliers.tolist()}")    # [100]

# 方法3：Z-score——距离均值超过 N 个标准差
z_scores = (nums - nums.mean()) / nums.std()  # 标准化：(值 - 均值) / 标准差
print(f"Z-score：{z_scores.round(2).tolist()}")
outliers_z = nums[z_scores.abs() > 2]         # |Z| > 2 视为异常（通常用 2 或 3）
print(f"Z-score 异常值（|Z|>2）：{outliers_z.tolist()}")

# 异常值处理策略
print("\n异常值处理策略演示：")
nums_fixed = nums.copy()
cap_upper  = Q3 + 1.5 * IQR                   # 上界（用于截断）

# 策略A：删除
nums_drop = nums[nums <= cap_upper]
print(f"  A.删除：{nums_drop.tolist()}")

# 策略B：截断（Winsorizing）：超界值替换为边界值
nums_clip = nums.clip(lower=lower, upper=cap_upper)
print(f"  B.截断：{nums_clip.tolist()}")       # 100 变成 upper 的值

# 策略C：替换为均值/中位数
nums_fill = nums.copy()
nums_fill[nums_fill > cap_upper] = nums[nums <= cap_upper].median()
print(f"  C.中位数替换：{nums_fill.tolist()}")

# ── 1-4 数据类型转换与字符串清洗 ─────────────────────

print("\n── 类型转换与字符串清洗 ──")

messy = pd.DataFrame({
    "金额":  ["¥1,299.00", "¥  89.50", "¥ 3,450", "N/A"],  # 含货币符号/空格/逗号
    "日期":  ["2024-04-01", "2024/04/02", "20240403", "2024-04-04"],  # 多种格式
    "评分":  ["4.5星", "3.0星", "5.0星", "2.5星"],                    # 含汉字后缀
})

# 清洗金额列：去掉 ¥ 符号、空格、逗号，再转 float
messy["金额_clean"] = (
    messy["金额"]
    .str.replace("¥", "", regex=False)         # 去掉 ¥（regex=False 视为普通字符）
    .str.replace(",", "", regex=False)          # 去掉千位逗号
    .str.strip()                               # 去掉两端空白
    .replace("N/A", np.nan)                   # 把 "N/A" 替换为真正的 NaN
    .astype(float)                             # 转为浮点数
)
print("金额清洗：", messy["金额_clean"].tolist())  # [1299.0, 89.5, 3450.0, nan]

# 清洗日期列：to_datetime 自动识别多种格式（format='mixed' 允许混合格式）
messy["日期_clean"] = pd.to_datetime(messy["日期"], format="mixed")
print("日期清洗：", messy["日期_clean"].dt.strftime("%Y-%m-%d").tolist())

# 清洗评分列：只保留数字部分
messy["评分_clean"] = messy["评分"].str.extract(r"(\d+\.?\d*)").astype(float)  # 正则提取数字
print("评分清洗：", messy["评分_clean"].tolist())  # [4.5, 3.0, 5.0, 2.5]

# ══════════════════════════════════════════════════════
# 二、分组聚合：groupby、agg、pivot_table
# ══════════════════════════════════════════════════════

print("\n══ 二、分组聚合 ══")

# 构造销售数据（后面各节复用）
np.random.seed(42)
N = 100
sales = pd.DataFrame({
    "日期":   pd.date_range("2024-01-01", periods=N, freq="D"),  # 日期序列
    "大区":   np.random.choice(["华北","华南","华东","西部"], N),
    "城市":   np.random.choice(["北京","上海","广州","深圳","成都","西安"], N),
    "销售员": [f"销售{i%8+1:02d}" for i in range(N)],
    "产品":   np.random.choice(["A产品","B产品","C产品"], N,
                                p=[0.4, 0.35, 0.25]),            # 非均匀概率
    "数量":   np.random.randint(10, 200, N),
    "单价":   np.random.choice([99.0, 199.0, 299.0], N),
})
sales["金额"]    = sales["数量"] * sales["单价"]
sales["季度"]    = sales["日期"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
sales["月份"]    = sales["日期"].dt.month
print(f"销售数据：{sales.shape}")
print(sales.head(3))

# ── 2-1 groupby 基础 ─────────────────────────────────

print("\n── groupby 基础 ──")

# groupby()：按一列或多列分组，返回 GroupBy 对象（惰性，不立即计算）
# 链式调用聚合函数：.sum() .mean() .count() .max() .min() .std() 等

# 单列分组
region_sum = sales.groupby("大区")["金额"].sum().sort_values(ascending=False)
print("各大区总金额：")
print(region_sum.apply(lambda x: f"¥{x:,.0f}"))   # apply 格式化为货币

# 多列分组
region_prod = sales.groupby(["大区", "产品"])["金额"].sum()
print("\n大区×产品 金额：")
print(region_prod.unstack(fill_value=0))           # unstack：把最内层索引转为列（透视）

# size()：统计每组的行数（比 count() 更简洁，count 会跳过 NaN）
print("\n各产品销售次数：")
print(sales.groupby("产品").size().rename("订单数"))

# 分组后访问原始数据
for name, group in sales.groupby("大区"):          # 遍历每个分组
    print(f"  {name}：{len(group)}条，均价¥{group['金额'].mean():.0f}")

# ── 2-2 agg：多函数聚合 ──────────────────────────────

print("\n── agg 多函数聚合 ──")

# agg（aggregate）：对每个分组应用多个聚合函数，返回多级列 DataFrame
region_agg = sales.groupby("大区")["金额"].agg(
    总金额="sum",                              # 别名="聚合函数名（字符串）"
    均值="mean",
    最大值="max",
    最小值="min",
    订单数="count",
    标准差="std",
)
print("agg 多指标：")
print(region_agg.round(1))

# 对不同列应用不同函数（字典形式）
multi_col_agg = sales.groupby("产品").agg({
    "金额": ["sum", "mean", "count"],          # 金额列：求和、均值、计数
    "数量": ["sum", "max"],                    # 数量列：求和、最大值
    "单价": "first",                           # 单价列：取第一个值
})
print("\n多列多函数：")
print(multi_col_agg.round(1))

# 自定义聚合函数
def cv(x):                                    # 变异系数（Coefficient of Variation）= std/mean
    return x.std() / x.mean() if x.mean() != 0 else 0   # 衡量相对离散程度

custom_agg = sales.groupby("大区")["金额"].agg(["mean", cv]).round(3)
custom_agg.columns = ["均值", "变异系数"]     # 重命名列
print("\n自定义聚合函数：")
print(custom_agg)

# transform：聚合结果广播回原 DataFrame（保持形状不变）
# 常用于"在原表中添加分组统计列"，不改变行数
sales["大区均值"] = sales.groupby("大区")["金额"].transform("mean").round(1)
sales["高于大区均值"] = sales["金额"] > sales["大区均值"]   # 布尔列
print(f"\n高于各自大区均值的订单数：{sales['高于大区均值'].sum()}")

# filter：过滤整个分组（满足条件的组全部保留，否则全部删除）
# 保留总金额 > 200000 的大区的所有行
big_regions = sales.groupby("大区").filter(lambda g: g["金额"].sum() > 200000)
print(f"高金额大区订单数：{len(big_regions)}")
print(f"保留的大区：{big_regions['大区'].unique().tolist()}")

# ── 2-3 pivot_table：透视表 ──────────────────────────

print("\n── pivot_table ──")

# pivot_table 是 groupby + agg + unstack 的便利封装
# 参数：values=统计值列，index=行分组，columns=列分组，aggfunc=聚合函数
pt = pd.pivot_table(
    sales,
    values="金额",                            # 要聚合的列
    index="大区",                             # 行方向分组（唯一值成为行索引）
    columns="产品",                           # 列方向分组（唯一值成为列标题）
    aggfunc="sum",                            # 聚合函数
    fill_value=0,                             # NaN 填 0（某大区没有某产品时）
    margins=True,                             # 加总计行/列（All 行和 All 列）
    margins_name="合计",                      # 总计行/列的标题
)
print("产品×大区 金额透视表：")
print(pt.applymap(lambda x: f"¥{x:,.0f}") if hasattr(pt, 'applymap')
      else pt.map(lambda x: f"¥{x:,.0f}"))   # pandas 2.1+ 用 map，旧版用 applymap

# 多值透视表：同时统计金额和数量
pt_multi = pd.pivot_table(
    sales,
    values=["金额", "数量"],                  # 同时聚合两列
    index="季度",
    columns="产品",
    aggfunc={"金额": "sum", "数量": "mean"},  # 不同列用不同函数
    fill_value=0,
)
print("\n季度×产品 多值透视表：")
print(pt_multi.round(1))

# pivot（无聚合）：把"长表"变"宽表"（每个行/列组合只有一个值时用）
wide = pd.pivot_table(
    sales.groupby(["季度","产品"])["金额"].sum().reset_index(),
    values="金额", index="季度", columns="产品", aggfunc="sum"
)
print("\n季度×产品 金额宽表：")
print(wide.astype(int))

# melt：把"宽表"变"长表"（pivot 的逆操作）
long = wide.reset_index().melt(
    id_vars="季度",                           # 保持不变的列（作为标识符）
    var_name="产品",                           # 原来的列名变成这一列的值
    value_name="金额",                         # 原来的值变成这一列
)
print("\nmelt 宽转长（前6行）：")
print(long.head(6))

# ══════════════════════════════════════════════════════
# 三、数据合并：merge、concat、join
# ══════════════════════════════════════════════════════

print("\n══ 三、数据合并 ══")

# 构造三个相关的小表
orders = pd.DataFrame({
    "订单ID":  ["O001","O002","O003","O004","O005"],
    "客户ID":  ["C01","C02","C01","C03","C99"],   # C99 在 customers 中不存在
    "产品ID":  ["P01","P02","P01","P03","P02"],
    "数量":    [10, 5, 8, 3, 12],
})
customers = pd.DataFrame({
    "客户ID":  ["C01","C02","C03","C04"],         # C04 在 orders 中不存在
    "姓名":    ["小明","小红","小刚","小李"],
    "城市":    ["北京","上海","广州","深圳"],
    "等级":    ["金牌","银牌","银牌","铜牌"],
})
products = pd.DataFrame({
    "产品ID":  ["P01","P02","P03"],
    "产品名":  ["苹果","香蕉","橙子"],
    "单价":    [5.5, 3.2, 4.8],
})

print("订单表：\n", orders)
print("客户表：\n", customers)
print("产品表：\n", products)

# ── 3-1 merge：类似 SQL 的 JOIN ───────────────────────

print("\n── merge ──")

# inner join（默认）：只保留两表都有的键
inner = pd.merge(orders, customers, on="客户ID")   # on 指定连接键（两表同名列）
print(f"inner join：{len(inner)} 行（C99 和 C04 都被丢弃）")
print(inner)

# left join：以左表为准，右表没有的填 NaN
left = pd.merge(orders, customers, on="客户ID", how="left")
print(f"\nleft join：{len(left)} 行（C99 保留，城市为 NaN）")
print(left)

# right join：以右表为准
right = pd.merge(orders, customers, on="客户ID", how="right")
print(f"\nright join：{len(right)} 行（C04 保留，订单信息为 NaN）")
print(right)

# outer join：保留两表所有行，不匹配的填 NaN
outer = pd.merge(orders, customers, on="客户ID", how="outer")
print(f"\nouter join：{len(outer)} 行（C99 和 C04 都保留）")
print(outer)

# 链式 merge：连接多张表（先 orders+customers，再 +products）
full = (orders
        .merge(customers, on="客户ID",  how="left")  # 先关联客户信息
        .merge(products,  on="产品ID",  how="left")  # 再关联产品信息
       )
full["金额"] = full["数量"] * full["单价"]            # 在合并后的宽表里计算金额
print("\n三表合并后：")
print(full)

# 两表列名不同时：用 left_on / right_on 分别指定
orders2 = orders.rename(columns={"客户ID": "cid"})    # 左表列名是 cid
merged_diff = pd.merge(orders2, customers,
                       left_on="cid", right_on="客户ID",  # 分别指定
                       how="inner")
print(f"\n不同列名 merge：{merged_diff.columns.tolist()}")

# suffixes：两表有同名列时自动加后缀区分
orders_p = orders.merge(products, on="产品ID")
orders_p2 = orders_p.copy()
orders_p2["数量"] = orders_p2["数量"] * 2             # 制造同名列冲突
conflict = pd.merge(orders_p, orders_p2, on="订单ID",
                    suffixes=("_原", "_新"))           # 默认后缀是 _x 和 _y
print(f"\n后缀处理同名列：{[c for c in conflict.columns if '数量' in c]}")

# ── 3-2 concat：堆叠拼接 ─────────────────────────────

print("\n── concat ──")

# 同结构的 DataFrame 上下拼接（axis=0，默认）
df_q1 = pd.DataFrame({"月": [1,2,3], "销售额": [100, 120, 95]})
df_q2 = pd.DataFrame({"月": [4,5,6], "销售额": [130, 115, 140]})
df_q3 = pd.DataFrame({"月": [7,8,9], "销售额": [150, 145, 160]})

combined = pd.concat([df_q1, df_q2, df_q3], ignore_index=True)   # ignore_index 重置行号
print("上下堆叠（ignore_index）：")
print(combined)

# keys 参数：给每段数据加多级索引标签（便于追溯来源）
labeled = pd.concat([df_q1, df_q2], keys=["Q1", "Q2"])
print("\n带 keys 标签：")
print(labeled)

# axis=1：左右拼接（按列拼接）
df_a = pd.DataFrame({"A": [1,2,3]})
df_b = pd.DataFrame({"B": [4,5,6]})
side_by_side = pd.concat([df_a, df_b], axis=1)   # 横向拼接
print("\n横向拼接（axis=1）：")
print(side_by_side)

# join 参数：拼接时如何处理索引不一致
df_x = pd.DataFrame({"X": [1,2]}, index=[0,1])
df_y = pd.DataFrame({"Y": [3,4]}, index=[1,2])
print("\njoin='outer'（保留所有索引）：")
print(pd.concat([df_x, df_y], axis=1, join="outer"))   # 不匹配的位置填 NaN
print("\njoin='inner'（只保留公共索引）：")
print(pd.concat([df_x, df_y], axis=1, join="inner"))   # 只有索引 1 共有

# ── 3-3 join：按索引合并 ─────────────────────────────

print("\n── join ──")

# join() 默认按行索引对齐合并（类似 merge 的 left join）
# 适合"两表已按同一索引排好"的场景
df_main = pd.DataFrame({"语文":[85,92,78]}, index=["小明","小红","小刚"])
df_extra = pd.DataFrame({"数学":[90,88,82],"英语":[78,95,68]},
                         index=["小明","小刚","小红"])  # 顺序不同无所谓，按索引对齐
joined = df_main.join(df_extra)               # 默认 how='left'，按 df_main 的索引
print("join 按索引合并：")
print(joined)

# ══════════════════════════════════════════════════════
# 四、时间序列处理
# ══════════════════════════════════════════════════════

print("\n══ 四、时间序列 ══")

# ── 4-1 创建时间序列 ──────────────────────────────────

print("\n── 创建时间序列 ──")

# pd.date_range：生成等间隔日期序列
daily   = pd.date_range("2024-01-01", periods=10, freq="D")     # 每日
monthly = pd.date_range("2024-01", periods=12, freq="ME")        # 每月末
hourly  = pd.date_range("2024-04-20 00:00", periods=24, freq="h")  # 每小时
bizday  = pd.date_range("2024-01-01", periods=10, freq="B")      # 仅工作日

print(f"每日 10 天：{daily[:3].tolist()} ...")
print(f"每月末 12 个：{[d.strftime('%Y-%m') for d in monthly]}")
print(f"工作日 10 天：{[d.strftime('%m-%d') for d in bizday]}")

# pd.to_datetime：把字符串/整数转换为 Timestamp
ts1 = pd.to_datetime("2024-04-20")
ts2 = pd.to_datetime("2024/04/20 15:30")
ts3 = pd.to_datetime(20240420, format="%Y%m%d")  # 整数格式
print(f"\nTimestamp：{ts1}  {ts2}  {ts3}")

# ── 4-2 dt 访问器：提取时间分量 ──────────────────────

print("\n── dt 访问器 ──")

# DatetimeIndex 的常用属性
ts_series = pd.Series(pd.date_range("2024-01-15", periods=6, freq="ME"))
print("日期序列：", ts_series.dt.strftime("%Y-%m-%d").tolist())
print("年：",   ts_series.dt.year.tolist())
print("月：",   ts_series.dt.month.tolist())
print("季度：", ts_series.dt.quarter.tolist())
print("星期几（0=周一）：", ts_series.dt.dayofweek.tolist())
print("是否月末：", ts_series.dt.is_month_end.tolist())
print("是否季末：", ts_series.dt.is_quarter_end.tolist())

# strftime / strptime：时间格式化与解析
dates_str = pd.Series(["20240101", "20240201", "20240301"])
parsed    = pd.to_datetime(dates_str, format="%Y%m%d")           # 解析
formatted = parsed.dt.strftime("%Y年%m月%d日")                    # 格式化
print("\n解析后格式化：", formatted.tolist())

# Timedelta：时间差
from datetime import timedelta
now = pd.Timestamp("2024-04-20")
print(f"\n两周后：{now + timedelta(weeks=2)}")
print(f"30天前：{now - pd.Timedelta(days=30)}")

# 两个时间相减得 Timedelta
start = pd.to_datetime("2024-01-01")
end   = pd.to_datetime("2024-04-20")
diff  = end - start                           # Timedelta 对象
print(f"相差：{diff.days} 天")

# ── 4-3 时间索引：时间序列的切片 ─────────────────────

print("\n── 时间索引切片 ──")

# 把时间列设为索引，才能使用时间切片功能
ts_idx = pd.DataFrame({
    "日期":  pd.date_range("2024-01-01", periods=120, freq="D"),
    "销售额": np.random.randint(100, 500, 120),
}).set_index("日期")                          # 设置时间索引

print(f"全部数据：{ts_idx.shape}")

# 字符串切片（只有 DatetimeIndex 才支持这种写法）
jan = ts_idx.loc["2024-01"]                    # 只取 1 月份的数据（pandas 2.x 须用 .loc）
print(f"1月数据：{len(jan)} 天")

q1 = ts_idx.loc["2024-01":"2024-03"]         # 取 Q1（1月~3月）
print(f"Q1 数据：{len(q1)} 天")

# 单个 Timestamp 访问
day = ts_idx.loc["2024-02-15"]               # 取特定某一天
print(f"2月15日销售额：{day['销售额']}")

# ── 4-4 resample：时间重采样 ──────────────────────────

print("\n── resample ──")

# resample(rule)：把时间序列按新频率聚合
# rule 常用值：'D'=日  'W'=周  'ME'=月末  'QE'=季末  'YE'=年末

# 日数据 → 周汇总
weekly_sum = ts_idx.resample("W")["销售额"].sum()    # 按自然周求和
print("按周汇总（前4周）：")
print(weekly_sum.head(4))

# 日数据 → 月汇总（多个聚合函数）
monthly_agg = ts_idx.resample("ME")["销售额"].agg(
    合计="sum", 均值="mean", 最高="max", 最低="min"
).round(1)
print("\n按月汇总：")
print(monthly_agg)

# 上采样（低频→高频）：日 → 小时，用 ffill 向前填充
daily_vals = pd.Series(
    [100, 200, 150],
    index=pd.date_range("2024-04-01", periods=3, freq="D")
)
hourly_vals = daily_vals.resample("h").ffill()  # 每小时都等于当天的值
print(f"\n上采样（日→小时）前3天：{len(hourly_vals)} 个小时点")

# 滚动窗口（rolling window）：移动平均、移动标准差
ts_1d = ts_idx["销售额"]
ma7  = ts_1d.rolling(window=7).mean()         # 7日移动平均
ma30 = ts_1d.rolling(window=30).mean()        # 30日移动平均（前30天为 NaN）
print(f"\n7日移动平均（后5行）：{ma7.tail().round(1).tolist()}")
print(f"30日移动平均（后5行）：{ma30.tail().round(1).tolist()}")

# expanding：扩展窗口（从第1行到当前行的累积统计）
cum_mean = ts_1d.expanding().mean()           # 截至当日的累积均值
print(f"累积均值（最后3个）：{cum_mean.tail(3).round(1).tolist()}")

# ── 4-5 时区处理 ──────────────────────────────────────

print("\n── 时区处理 ──")

ts_naive = pd.Timestamp("2024-04-20 12:00:00")          # 无时区（naive）
ts_utc   = ts_naive.tz_localize("UTC")                  # 设置时区为 UTC
ts_cst   = ts_utc.tz_convert("Asia/Shanghai")            # 转换为北京时间（UTC+8）
ts_ny    = ts_utc.tz_convert("America/New_York")         # 转换为纽约时间（UTC-4/5）
print(f"UTC：       {ts_utc}")
print(f"北京时间：  {ts_cst}")
print(f"纽约时间：  {ts_ny}")

# ══════════════════════════════════════════════════════
# 五、综合实战：销售数据完整分析
# ══════════════════════════════════════════════════════

print("\n══ 五、综合实战：销售分析 ══")

# ── Step 0：生成模拟销售数据 ─────────────────────────

np.random.seed(99)
N2 = 200
products_list = ["笔记本","手机","平板","耳机","充电器"]
regions_list  = ["华北","华南","华东","西部","东北"]
channels_list = ["线上","线下","代理商"]

raw_sales = pd.DataFrame({
    "订单日期":  pd.date_range("2024-01-01", periods=N2, freq="D")[:N2],
    "大区":      np.random.choice(regions_list,  N2),
    "渠道":      np.random.choice(channels_list, N2, p=[0.5, 0.3, 0.2]),
    "产品":      np.random.choice(products_list, N2),
    "销售数量":  np.random.randint(1, 50, N2),
    "客单价":    np.random.choice([299,499,799,1299,29], N2),
})

# 随机制造一些缺失值和重复行（真实数据常见的问题）
dup_idx = np.random.choice(N2, size=10, replace=False)
raw_sales = pd.concat([raw_sales, raw_sales.iloc[dup_idx]],    # 添加重复行
                       ignore_index=True)
null_idx  = np.random.choice(len(raw_sales), size=8, replace=False)
raw_sales.loc[null_idx, "销售数量"] = np.nan                    # 注入缺失值

print(f"原始数据：{raw_sales.shape}，含重复行/缺失值")

# ── Step 1：数据清洗 ──────────────────────────────────

df_s = raw_sales.copy()
df_s = df_s.drop_duplicates()                # 删除完全重复行
df_s["销售数量"] = df_s["销售数量"].fillna(df_s["销售数量"].median())  # 中位数填充

# 类型整理
df_s["订单日期"] = pd.to_datetime(df_s["订单日期"])
df_s["销售数量"] = df_s["销售数量"].astype(int)

# 派生列
df_s["销售金额"] = df_s["销售数量"] * df_s["客单价"]
df_s["月份"]    = df_s["订单日期"].dt.month
df_s["季度"]    = df_s["订单日期"].dt.quarter.map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
df_s["星期"]    = df_s["订单日期"].dt.day_name()   # 英文星期名
df_s.reset_index(drop=True, inplace=True)

print(f"清洗后：{df_s.shape}，无重复无缺失")

# ── Step 2：整体概览 ──────────────────────────────────

total_rev  = df_s["销售金额"].sum()
total_ord  = len(df_s)
avg_order  = df_s["销售金额"].mean()
date_range = f"{df_s['订单日期'].min().strftime('%Y-%m-%d')} ~ {df_s['订单日期'].max().strftime('%Y-%m-%d')}"

print(f"\n─ 整体概览 ─")
print(f"  日期范围：{date_range}")
print(f"  总订单数：{total_ord:,}")
print(f"  总销售额：¥{total_rev:,.0f}")
print(f"  平均客单：¥{avg_order:,.1f}")

# ── Step 3：分组分析——大区 ────────────────────────────

print("\n─ 各大区汇总 ─")
region_summary = df_s.groupby("大区").agg(
    订单数  = ("销售金额", "count"),
    总金额  = ("销售金额", "sum"),
    均单价  = ("销售金额", "mean"),
    总数量  = ("销售数量", "sum"),
).sort_values("总金额", ascending=False).round(1)

region_summary["占比%"] = (region_summary["总金额"] /
                           region_summary["总金额"].sum() * 100).round(1)
print(region_summary.to_string())

# ── Step 4：分组分析——产品 ────────────────────────────

print("\n─ 各产品汇总 ─")
prod_summary = df_s.groupby("产品").agg(
    订单数 = ("销售金额", "count"),
    总金额 = ("销售金额", "sum"),
    均数量 = ("销售数量", "mean"),
).sort_values("总金额", ascending=False).round(1)
print(prod_summary.to_string())

# ── Step 5：透视表——大区 × 产品 ───────────────────────

print("\n─ 大区×产品 销售额透视表 ─")
pt_main = pd.pivot_table(
    df_s,
    values="销售金额",
    index="大区",
    columns="产品",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="合计",
)
# 格式化：数字转"万元"字符串
def to_wan(x):
    return f"{x/10000:.1f}万" if x >= 10000 else f"¥{x:.0f}"

print(pt_main.applymap(to_wan) if hasattr(pt_main, 'applymap')
      else pt_main.map(to_wan))

# ── Step 6：时间趋势——月度走势 ───────────────────────

print("\n─ 月度趋势 ─")
monthly_trend = (df_s.set_index("订单日期")
                      .resample("ME")["销售金额"]
                      .agg(["sum","count","mean"])
                      .round(1))
monthly_trend.columns = ["月销售额","订单数","均单价"]
monthly_trend.index   = monthly_trend.index.strftime("%Y-%m")   # 格式化索引为 "年-月"
print(monthly_trend.to_string())

# ── Step 7：渠道分析 ──────────────────────────────────

print("\n─ 渠道×产品 订单量透视 ─")
channel_pt = pd.pivot_table(
    df_s,
    values="销售数量",
    index="渠道",
    columns="产品",
    aggfunc="count",     # 统计订单数（而非数量之和）
    fill_value=0,
    margins=True,
    margins_name="合计",
)
print(channel_pt.to_string())

# ── Step 8：找出高价值订单 ───────────────────────────

print("\n─ 高价值订单（Top 10）─")
top_orders = (df_s
              .nlargest(10, "销售金额")             # nlargest：取最大的 N 行
              [["订单日期","大区","渠道","产品","销售数量","客单价","销售金额"]]
              .reset_index(drop=True))
print(top_orders.to_string(index=False))

# ── Step 9：保存报告 ──────────────────────────────────

out_excel = WORK_DIR / "sales_report.xlsx"
with pd.ExcelWriter(out_excel, engine="openpyxl") as writer:
    df_s.to_excel(writer, sheet_name="明细数据", index=False)
    region_summary.to_excel(writer, sheet_name="大区汇总")
    prod_summary.to_excel(writer, sheet_name="产品汇总")
    pt_main.to_excel(writer, sheet_name="大区产品透视")
    monthly_trend.to_excel(writer, sheet_name="月度趋势")

print(f"\n报告保存：{out_excel.name}（{out_excel.stat().st_size:,} 字节）")

# ── 清理 ──────────────────────────────────────────────
import shutil
shutil.rmtree(WORK_DIR)
print(f"已清理：{WORK_DIR.name}/")
