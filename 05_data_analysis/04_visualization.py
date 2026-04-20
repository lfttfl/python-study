# -*- coding: utf-8 -*-
# ============================================================
# 05_data_analysis/04_visualization.py
# Matplotlib 数据可视化练习
# ============================================================

import matplotlib                                      # 导入 matplotlib 核心模块
matplotlib.use("Agg")                                  # 必须在 pyplot 之前设置非交互后端（直接保存文件）
import matplotlib.pyplot as plt                        # pyplot 是最常用的绘图接口，约定别名 plt
import matplotlib.gridspec as gridspec                 # gridspec 提供灵活的子图布局（类似合并单元格）
import matplotlib.ticker as ticker                     # ticker 控制坐标轴刻度的显示格式
import matplotlib.patches as mpatches                  # patches 用于创建自定义图例色块
import numpy as np                                     # numpy 用于生成示例数据和数学运算
import pandas as pd                                    # pandas 用于处理结构化销售数据
from pathlib import Path                               # pathlib 提供跨平台路径操作
import shutil                                          # shutil 用于最后清理临时目录
import warnings                                        # warnings 模块用于过滤无关警告

warnings.filterwarnings("ignore")                      # 忽略字体查找等非关键警告，保持输出简洁

# ── 中文字体配置（Windows）───────────────────────────────────
# matplotlib 默认字体不含中文，需指定系统字体，否则中文显示为方块
plt.rcParams["font.family"] = ["Microsoft YaHei",     # 优先：微软雅黑（Windows 内置）
                                "SimHei",              # 备选：黑体（Windows 内置）
                                "DejaVu Sans"]         # 兜底：英文字体（确保不报错）
plt.rcParams["axes.unicode_minus"] = False             # 修复负号 '-' 被渲染为方块的问题
plt.rcParams["figure.dpi"] = 100                      # 全局屏幕显示分辨率（100 DPI）
plt.rcParams["savefig.dpi"] = 150                     # 保存文件分辨率（150 DPI，比屏幕更清晰）
plt.rcParams["figure.facecolor"] = "white"            # 图像背景统一设为白色

# ── 动态检测可用的 seaborn 样式名称 ──────────────────────────
# matplotlib 3.6+ 将 seaborn 样式重命名为 seaborn-v0_8-xxx
_sg = next((s for s in plt.style.available          # 从所有可用样式中查找
             if "seaborn" in s and "whitegrid" in s), # 包含 seaborn 和 whitegrid 关键词的样式
            "ggplot")                                  # 找不到则回退到 ggplot 样式

# ── 输出目录 ─────────────────────────────────────────────────
OUT = Path("tmp_viz")                                  # 定义临时输出目录名称
OUT.mkdir(exist_ok=True)                               # exist_ok=True：目录已存在时不报错

print("Matplotlib 版本：", matplotlib.__version__)     # 打印版本，便于排查兼容性问题

# ============================================================
# 一、基础图表
# ============================================================
print("\n══ 一、基础图表 ══")

# ── 1-1 折线图（Line Chart）─────────────────────────────────
print("── 1-1 折线图 ──")

x = np.arange(1, 13)                                  # x 轴数据：1~12 月
y_2023 = np.array([42, 38, 55, 61, 58, 72,
                   68, 75, 80, 65, 90, 110])          # 2023 年各月销售额（万元）
y_2024 = np.array([50, 45, 62, 70, 65, 85,
                   78, 88, 95, 72, 105, 130])         # 2024 年各月销售额（万元）

fig, ax = plt.subplots(figsize=(10, 5))               # 创建画布（figure）和坐标轴（axes）

ax.plot(x, y_2023,                                    # x 轴数据、y 轴数据
        color="#4C72B0",                              # 线条颜色（十六进制 RGB）
        linewidth=2,                                   # 线条宽度（单位：磅）
        linestyle="-",                                 # 线型：实线（-- 虚线，-. 点划线，: 点线）
        marker="o",                                    # 数据点标记：圆形（s=方，^=三角）
        markersize=6,                                  # 标记大小
        label="2023年")                               # 图例标签文字

ax.plot(x, y_2024,                                    # 第二条折线
        color="#DD8452",                              # 橙色，与第一条线颜色区分
        linewidth=2,                                   # 线宽
        linestyle="--",                                # 虚线样式
        marker="s",                                   # 方形标记
        markersize=6,                                  # 标记大小
        label="2024年")                               # 图例标签

ax.set_title("月度销售额对比（2023 vs 2024）",         # 图表标题
             fontsize=14, pad=12)                      # pad 控制标题与图顶部的间距
ax.set_xlabel("月份", fontsize=12)                    # x 轴标签
ax.set_ylabel("销售额（万元）", fontsize=12)          # y 轴标签
ax.set_xticks(x)                                      # 设置 x 轴刻度位置
ax.set_xticklabels([f"{m}月" for m in x])            # 将数字刻度替换为"X月"格式
ax.legend(loc="upper left", fontsize=11)              # 显示图例，loc 控制位置
ax.grid(axis="y", alpha=0.4, linestyle="--")          # 显示水平网格线，alpha 控制透明度
ax.set_ylim(0, 150)                                   # 手动设置 y 轴范围，留顶部注释空间

ax.annotate(f"{y_2024[-1]}万",                        # 在最后数据点旁添加文字注释
            xy=(12, y_2024[-1]),                      # 箭头指向的坐标（数据点位置）
            xytext=(10.8, y_2024[-1] + 10),           # 注释文字的坐标（偏移后的位置）
            arrowprops=dict(arrowstyle="->",          # 箭头样式（-> 表示单箭头）
                            color="gray"),             # 箭头颜色
            fontsize=10, color="#DD8452")              # 注释字体大小和颜色

fig.tight_layout()                                    # 自动调整子图间距，防止标签被裁剪
fig.savefig(OUT / "01_line_chart.png")               # 将图像保存为 PNG 文件
plt.close(fig)                                        # 关闭画布对象，释放内存
print(f"  已保存：{OUT}/01_line_chart.png")


# ── 1-2 柱状图（Bar Chart）─────────────────────────────────
print("── 1-2 柱状图 ──")

categories = ["华东", "华南", "华北", "西部", "东北"]  # x 轴类别标签
sales_2023 = [420, 490, 380, 610, 350]                # 2023 年各大区销售额
sales_2024 = [510, 560, 430, 680, 420]                # 2024 年各大区销售额
x_pos = np.arange(len(categories))                    # 生成 x 轴刻度位置数组（0,1,2,3,4）
bar_width = 0.35                                       # 每根柱子的宽度（两组柱共占 0.7）

fig, ax = plt.subplots(figsize=(10, 5))               # 创建画布

bars1 = ax.bar(x_pos - bar_width / 2,                 # 第一组柱子向左偏移半个宽度
               sales_2023,                             # 柱子高度
               width=bar_width,                        # 柱宽
               color="#4C72B0",                       # 蓝色
               alpha=0.85,                             # 透明度（0=全透明，1=不透明）
               label="2023年",                        # 图例标签
               edgecolor="white", linewidth=0.8)       # 柱边框颜色和宽度

bars2 = ax.bar(x_pos + bar_width / 2,                 # 第二组柱子向右偏移半个宽度
               sales_2024,                             # 柱子高度
               width=bar_width,                        # 柱宽
               color="#DD8452",                       # 橙色
               alpha=0.85,                             # 透明度
               label="2024年",                        # 图例标签
               edgecolor="white", linewidth=0.8)       # 柱边框

for bar in bars1:                                      # 遍历第一组所有柱子，添加柱顶数值
    h = bar.get_height()                               # 获取柱子高度值
    ax.text(bar.get_x() + bar.get_width() / 2,        # 文字 x 坐标（柱子中心）
            h + 8, f"{h}",                             # 文字 y 坐标（柱顶上方 8 单位）和内容
            ha="center", va="bottom", fontsize=9)      # 水平居中，垂直底部对齐

for bar in bars2:                                      # 遍历第二组柱子
    h = bar.get_height()                               # 获取柱高
    ax.text(bar.get_x() + bar.get_width() / 2,        # 柱子中心 x
            h + 8, f"{h}",                             # 柱顶上方文字
            ha="center", va="bottom",                  # 对齐方式
            fontsize=9, color="#DD8452")               # 与柱子同色

ax.set_title("各大区销售额对比", fontsize=14, pad=12) # 标题
ax.set_xlabel("大区", fontsize=12)                    # x 轴标签
ax.set_ylabel("销售额（万元）", fontsize=12)          # y 轴标签
ax.set_xticks(x_pos)                                  # x 轴刻度位置
ax.set_xticklabels(categories, fontsize=11)           # x 轴刻度文字
ax.legend(fontsize=11)                                # 显示图例
ax.set_ylim(0, 780)                                   # y 轴上限，留足标注空间
ax.grid(axis="y", alpha=0.3, linestyle="--")          # 水平辅助网格线

fig.tight_layout()                                    # 自动调整布局
fig.savefig(OUT / "02_bar_chart.png")                # 保存 PNG
plt.close(fig)                                        # 关闭释放内存
print(f"  已保存：{OUT}/02_bar_chart.png")


# ── 1-3 散点图（Scatter Chart）─────────────────────────────
print("── 1-3 散点图 ──")

rng = np.random.default_rng(seed=42)                  # 固定随机种子保证结果可复现
n = 80                                                 # 样本点数量
ad_spend  = rng.uniform(10, 100, n)                   # 广告投入（万元）：均匀分布
sales_rev = ad_spend * rng.uniform(3, 8, n) + rng.normal(0, 30, n)  # 销售额 = 线性关系 + 噪声

region = rng.choice(["华东", "华南", "华北", "西部"], n)  # 随机大区分类
color_map = {"华东": "#4C72B0", "华南": "#DD8452",    # 大区 → 颜色映射字典
             "华北": "#55A868", "西部": "#C44E52"}     # 绿色和红色
point_colors = [color_map[r] for r in region]         # 按每个点的大区生成颜色列表

fig, ax = plt.subplots(figsize=(8, 6))                # 创建画布

ax.scatter(ad_spend, sales_rev,                        # x 轴：广告投入，y 轴：销售额
           c=point_colors,                             # 点颜色（颜色列表）
           s=60,                                       # 点大小（面积单位，越大点越大）
           alpha=0.7,                                  # 透明度，重叠时仍可见各点
           edgecolors="white", linewidths=0.5)         # 点边框白色，宽度0.5

coef = np.polyfit(ad_spend, sales_rev, 1)              # 最小二乘一次多项式拟合（y = kx + b）
poly = np.poly1d(coef)                                 # 构造多项式函数对象
x_line = np.linspace(ad_spend.min(), ad_spend.max(), 100)  # 趋势线均匀 100 个点
r2 = np.corrcoef(ad_spend, sales_rev)[0, 1] ** 2      # 计算 R²（皮尔逊相关系数的平方）
ax.plot(x_line, poly(x_line),                         # 绘制趋势线
        color="black", linewidth=1.5,                  # 黑色
        linestyle="--", alpha=0.6,                     # 虚线，半透明
        label=f"趋势线（R²≈{r2:.2f}）")              # 标签含 R² 值

# 手动构建图例（scatter 用颜色区分大区，无法自动生成分类图例）
legend_handles = [mpatches.Patch(color=v, label=k)    # 每个大区创建一个颜色块 Patch
                  for k, v in color_map.items()]
legend_handles.append(                                 # 在颜色块图例后追加趋势线图例
    plt.Line2D([0], [0], color="black",               # 用 Line2D 模拟线条样式
               linewidth=1.5, linestyle="--",          # 与实际趋势线一致
               label=f"趋势线（R²≈{r2:.2f}）"))      # 标签

ax.legend(handles=legend_handles, loc="upper left", fontsize=10)  # 使用手动图例
ax.set_title("广告投入 vs 销售额（各大区）", fontsize=14, pad=12)  # 标题
ax.set_xlabel("广告投入（万元）", fontsize=12)         # x 轴标签
ax.set_ylabel("销售额（万元）", fontsize=12)          # y 轴标签
ax.grid(alpha=0.3, linestyle="--")                    # 显示网格线

fig.tight_layout()                                    # 调整布局
fig.savefig(OUT / "03_scatter_chart.png")            # 保存 PNG
plt.close(fig)                                        # 关闭释放内存
print(f"  已保存：{OUT}/03_scatter_chart.png")


# ── 1-4 饼图（Pie Chart）────────────────────────────────────
print("── 1-4 饼图 ──")

pie_labels  = ["手机", "平板", "笔记本", "耳机", "充电器"]  # 产品类别
pie_values  = [38, 22, 18, 13, 9]                           # 各产品销售占比
pie_colors  = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]  # 五种颜色
explode     = [0.06, 0, 0, 0, 0]                            # 突出第一个扇区（手机），偏移 0.06

fig, axes = plt.subplots(1, 2, figsize=(12, 6))       # 1 行 2 列：左标准饼图，右环形图

# 左图：标准饼图
wedges1, texts1, pcts1 = axes[0].pie(
    pie_values,                                        # 各扇区数值（自动换算百分比）
    labels=pie_labels,                                 # 扇区外侧文字标签
    explode=explode,                                   # 扇区突出偏移量列表
    colors=pie_colors,                                 # 各扇区颜色
    autopct="%1.1f%%",                                # 自动显示百分比（保留 1 位小数）
    pctdistance=0.75,                                  # 百分比文字距圆心的比例（0=圆心，1=边缘）
    startangle=90,                                     # 起始角度（90 = 从 12 点方向开始）
    shadow=True,                                       # 显示投影阴影效果
    wedgeprops=dict(edgecolor="white", linewidth=1.5)) # 扇区间白色分隔线

for p in pcts1:                                        # 调整百分比文字样式
    p.set_fontsize(10)                                 # 字体大小
    p.set_color("white")                               # 白色字体（在彩色背景上清晰可读）

axes[0].set_title("产品销售额占比（饼图）",            # 左图标题
                  fontsize=13, pad=15)                 # pad 控制标题距图的间距

# 右图：环形图（donut chart = width < 1 的饼图）
wedges2, texts2, pcts2 = axes[1].pie(
    pie_values,                                        # 数值数据
    labels=pie_labels,                                 # 标签
    colors=pie_colors,                                 # 颜色
    autopct="%1.1f%%",                                # 百分比格式
    pctdistance=0.82,                                  # 百分比位置稍远（在环带上）
    startangle=90,                                     # 起始角度
    wedgeprops=dict(edgecolor="white",                # 边框白色
                    linewidth=1.5,                     # 边框宽度
                    width=0.5))                        # width=0.5 → 环带宽度 50%，形成环形

for p in pcts2:                                        # 调整右图百分比样式
    p.set_fontsize(10)                                 # 字号
    p.set_color("white")                               # 白色

axes[1].text(0, 0, "产品\n占比",                       # 在环形中心添加说明文字
             ha="center", va="center",                 # 水平垂直居中
             fontsize=14, fontweight="bold",            # 加粗
             color="#333333")                          # 深灰色

axes[1].set_title("产品销售额占比（环形图）",          # 右图标题
                  fontsize=13, pad=15)

fig.tight_layout()                                    # 调整布局
fig.savefig(OUT / "04_pie_chart.png")                # 保存 PNG
plt.close(fig)                                        # 释放内存
print(f"  已保存：{OUT}/04_pie_chart.png")


# ============================================================
# 二、图表美化：样式、注释、参考线
# ============================================================
print("\n══ 二、图表美化 ══")

months = list(range(1, 13))                            # 月份 1~12
revenue = [58, 65, 72, 80, 78, 95,
           105, 98, 112, 88, 125, 145]                # 月度营收数据（万元）

with plt.style.context(_sg):                           # 临时切换为 seaborn/ggplot 样式
    fig, ax = plt.subplots(figsize=(11, 5))            # 在样式上下文中创建画布

    ax.fill_between(months, revenue,                   # 在折线下方填充颜色区域
                    alpha=0.12, color="#4C72B0")        # 低透明度填充，视觉上突出趋势

    ax.plot(months, revenue,                           # 绘制折线
            color="#4C72B0", linewidth=2.5,            # 线颜色和宽度
            marker="o", markersize=8,                  # 圆形标记，大小 8
            markerfacecolor="white",                   # 标记内部白色（空心效果）
            markeredgecolor="#4C72B0",                 # 标记边框颜色与线同色
            markeredgewidth=2,                         # 标记边框宽度
            zorder=3,                                  # 绘制层级（数值越大越在上层）
            label="月度营收")                          # 图例标签

    for m, r in zip(months, revenue):                 # 遍历每个月，在点上方添加数值标签
        ax.text(m, r + 3, f"{r}",                     # 文字位置（点上方 3 单位）和内容
                ha="center", fontsize=9, color="#333") # 居中，字号 9，深灰色

    peak_m = int(np.argmax(revenue)) + 1              # 最大营收所在月份（argmax 返回 0-based 索引）
    peak_v = max(revenue)                              # 最大营收值
    ax.annotate(f"峰值 {peak_v}万",                   # 峰值注释文字
                xy=(peak_m, peak_v),                   # 箭头指向坐标（峰值点）
                xytext=(peak_m - 2.5, peak_v + 14),   # 注释文字坐标（偏移）
                fontsize=11, color="red",              # 字号和颜色
                arrowprops=dict(arrowstyle="->",       # 箭头类型
                                color="red", lw=1.5)) # 箭头颜色和线宽

    avg = float(np.mean(revenue))                      # 计算平均营收
    ax.axhline(avg,                                    # axhline 绘制贯穿图表的水平参考线
               color="orange", linewidth=1.5,          # 橙色线
               linestyle=":", alpha=0.9,               # 点线样式，高透明度
               label=f"月均 {avg:.0f}万")             # 图例标签（保留整数）

    # y 轴刻度格式化：在数值后追加"万"单位
    ax.yaxis.set_major_formatter(                      # 设置 y 轴主刻度格式化器
        ticker.FuncFormatter(                          # FuncFormatter 接受函数 (value, pos) → str
            lambda v, _: f"{int(v)}万"))               # lambda 将数值转为"XX万"字符串

    ax.set_xticks(months)                             # 设置 x 轴刻度位置
    ax.set_xticklabels([f"{m}月" for m in months],   # 将数字替换为"X月"
                       fontsize=10)                    # 刻度字号
    ax.set_title("2024年月度营收趋势",                # 标题
                 fontsize=15, fontweight="bold", pad=15)  # 加粗，顶部间距
    ax.set_xlabel("月份", fontsize=12)                # x 轴标签
    ax.set_ylabel("营收（万元）", fontsize=12)        # y 轴标签
    ax.legend(fontsize=11, loc="upper left")          # 图例
    ax.set_ylim(40, 175)                              # y 轴范围（留顶部标注空间）

    fig.tight_layout()                                 # 调整布局
    fig.savefig(OUT / "05_styled_line.png")           # 保存 PNG
    plt.close(fig)                                     # 关闭
    print(f"  已保存：{OUT}/05_styled_line.png")


# ============================================================
# 三、多子图：subplot 与 GridSpec
# ============================================================
print("\n══ 三、多子图 ══")

# ── 3-1 plt.subplots 均匀网格 ──────────────────────────────
x_demo = np.linspace(0, 2 * np.pi, 100)               # 0~2π 均匀取 100 个点（用于三角函数演示）

fig, axes = plt.subplots(2, 2,                         # 创建 2 行 × 2 列共 4 个子图
                          figsize=(11, 8))              # 总画布宽 11 高 8 英寸

# 子图 [0,0]：sin 折线
axes[0, 0].plot(x_demo, np.sin(x_demo),               # 绘制 sin(x) 曲线
                color="#4C72B0", linewidth=2)           # 蓝色，线宽 2
axes[0, 0].set_title("sin(x)", fontsize=12)            # 子图标题
axes[0, 0].set_xlabel("x"); axes[0, 0].set_ylabel("y")  # 轴标签
axes[0, 0].grid(alpha=0.3)                             # 半透明网格线

# 子图 [0,1]：cos 虚线
axes[0, 1].plot(x_demo, np.cos(x_demo),               # 绘制 cos(x) 曲线
                color="#DD8452", linewidth=2,           # 橙色
                linestyle="--")                        # 虚线样式
axes[0, 1].set_title("cos(x)", fontsize=12)           # 标题
axes[0, 1].grid(alpha=0.3)                             # 网格线

# 子图 [1,0]：随机柱状图
bar_y = rng.integers(10, 50, 8)                        # 生成 8 个随机整数（10~49）作为柱高
axes[1, 0].bar(range(8), bar_y,                        # 8 根柱子
               color="#55A868", alpha=0.8,             # 绿色，透明度 0.8
               edgecolor="white")                      # 白色边框
axes[1, 0].set_title("随机柱状图", fontsize=12)        # 标题
axes[1, 0].set_xlabel("类别", fontsize=10)             # x 轴标签

# 子图 [1,1]：正态分布散点
sx = rng.normal(0, 1, 200)                             # 200 个 N(0,1) 正态随机数（x）
sy = rng.normal(0, 1, 200)                             # 200 个 N(0,1) 正态随机数（y）
axes[1, 1].scatter(sx, sy,                             # 散点图
                   alpha=0.5, s=20,                    # 半透明，点大小 20
                   color="#C44E52")                    # 红色
axes[1, 1].set_title("正态分布散点图", fontsize=12)    # 标题
axes[1, 1].set_xlabel("x"); axes[1, 1].set_ylabel("y")  # 轴标签

fig.suptitle("四种基础图表综合展示",                   # suptitle 为整张画布设置总标题
             fontsize=15, fontweight="bold")            # 加粗
fig.tight_layout()                                     # 自动调整各子图间距
fig.savefig(OUT / "06_subplots_grid.png",             # 保存 PNG
            bbox_inches="tight")                       # bbox_inches='tight' 防止标题被截断
plt.close(fig)                                         # 关闭
print(f"  已保存：{OUT}/06_subplots_grid.png")


# ── 3-2 GridSpec 不等大子图布局 ─────────────────────────────
# GridSpec 可让子图跨多行或多列，类似 Excel "合并单元格"
fig = plt.figure(figsize=(12, 8))                     # 直接创建画布（不预设子图）
gs  = gridspec.GridSpec(2, 3,                          # 定义 2 行 × 3 列网格
                        figure=fig,                    # 关联到指定画布
                        hspace=0.4,                    # 子图垂直间距（占高度比例）
                        wspace=0.35)                   # 子图水平间距（占宽度比例）

ax_top = fig.add_subplot(gs[0, :])                    # 第 0 行、全部列 → 跨 3 列的宽图
ax_bl  = fig.add_subplot(gs[1, 0])                    # 第 1 行第 0 列
ax_bm  = fig.add_subplot(gs[1, 1])                    # 第 1 行第 1 列
ax_br  = fig.add_subplot(gs[1, 2])                    # 第 1 行第 2 列

# 顶部宽图：月度趋势折线 + 面积填充
ax_top.fill_between(months, revenue, alpha=0.1, color="#4C72B0")  # 面积填充
ax_top.plot(months, revenue,                           # 折线
            color="#4C72B0", linewidth=2,              # 蓝色，线宽 2
            marker="o", markersize=6)                  # 圆形标记
ax_top.set_xticks(months)                             # x 刻度位置
ax_top.set_xticklabels([f"{m}月" for m in months], fontsize=9)  # 中文月份标签
ax_top.set_title("月度营收趋势（跨列主图）", fontsize=13)  # 子图标题
ax_top.grid(alpha=0.3)                                # 网格线

# 左下：大区柱状图（各柱不同颜色）
regions = ["华东", "华南", "华北", "西部"]            # 大区名称
reg_vals = [510, 560, 430, 680]                       # 各大区销售额
ax_bl.bar(regions, reg_vals,                           # 柱状图
          color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"],  # 每根柱不同颜色
          alpha=0.85, edgecolor="white")               # 透明度和边框
ax_bl.set_title("大区销售额", fontsize=11)            # 标题
ax_bl.set_ylabel("万元", fontsize=9)                  # y 轴标签
ax_bl.tick_params(axis="x", labelsize=9)              # x 刻度字号

# 中下：产品占比饼图
ax_bm.pie([38, 22, 18, 13, 9],                         # 数据
          labels=["手机", "平板", "笔记本", "耳机", "充电器"],  # 标签
          colors=pie_colors,                           # 颜色列表
          autopct="%1.0f%%",                           # 整数百分比（无小数点）
          startangle=90,                               # 起始角度
          textprops={"fontsize": 8})                   # 标签和百分比字号
ax_bm.set_title("产品占比", fontsize=11)              # 标题

# 右下：产品销量水平柱状图（barh = horizontal bar）
products_h = ["手机", "平板", "笔记本", "耳机", "充电器"]  # y 轴标签
quantities  = [1050, 820, 680, 750, 940]               # 各产品销量（件）
ax_br.barh(products_h, quantities,                     # barh 绘制水平柱（y=标签，x=数值）
           color="#8172B3", alpha=0.85,                # 紫色
           edgecolor="white")                          # 边框白色
ax_br.set_title("产品销量（件）", fontsize=11)         # 标题
ax_br.set_xlabel("件数", fontsize=9)                  # x 轴标签（水平柱图中 x 是数量）
ax_br.grid(axis="x", alpha=0.3)                       # 垂直方向网格线

fig.suptitle("业务数据综合看板（GridSpec 布局）",      # 整张画布总标题
             fontsize=15, fontweight="bold")            # 加粗
fig.savefig(OUT / "07_gridspec_layout.png",           # 保存 PNG
            bbox_inches="tight", dpi=150)              # 防截断，150 DPI
plt.close(fig)                                         # 关闭释放内存
print(f"  已保存：{OUT}/07_gridspec_layout.png")


# ============================================================
# 四、实战：模拟销售数据可视化
# ============================================================
print("\n══ 四、实战：销售数据可视化 ══")

# ── 生成模拟销售数据 ──────────────────────────────────────
np.random.seed(2024)                                   # 固定随机种子，确保每次运行结果一致
N = 200                                                # 订单总数

df = pd.DataFrame({
    "订单日期": pd.date_range("2024-01-01", periods=N, freq="D"),  # 从元旦起连续 200 天
    "大区":    np.random.choice(["华东","华南","华北","西部","东北"], N),  # 随机大区
    "产品":    np.random.choice(["手机","平板","笔记本","耳机","充电器"], N),  # 随机产品
    "渠道":    np.random.choice(["线上","线下","代理商"], N),       # 随机渠道
    "销售数量": np.random.randint(1, 50, N),           # 随机销量（1~49 件）
    "客单价":  np.random.choice([99, 299, 599, 999, 1299], N),     # 五种定价
})
df["销售金额"] = df["销售数量"] * df["客单价"]         # 金额 = 数量 × 单价
df["月份"]    = df["订单日期"].dt.to_period("M")       # 提取月份（Period 类型，如 2024-01）

print(f"  销售数据：{df.shape}，"
      f"日期范围 {df['订单日期'].min().date()}~{df['订单日期'].max().date()}")

# 按月汇总
monthly_df = (df.groupby("月份")["销售金额"]           # 按月分组，取销售金额列
              .sum()                                   # 求每月总金额
              .reset_index())                          # 重置索引变为普通 DataFrame
monthly_df["标签"] = (monthly_df["月份"]               # 月份标签：Period → 字符串 → 截取后两位
                      .astype(str).str[-2:] + "月")   # "2024-01" → "01" + "月" → "01月"
monthly_df["万元"] = (monthly_df["销售金额"] / 10000).round(1)  # 转换为万元，保留 1 位小数

# 按产品汇总
prod_df = (df.groupby("产品")
           .agg(订单数=("销售金额", "count"),          # 命名聚合：统计订单数
                总金额=("销售金额", "sum"),             # 总销售金额
                总数量=("销售数量", "sum"))             # 总销售数量
           .sort_values("总金额", ascending=False)     # 按总金额降序，重要产品排前面
           .reset_index())                             # 重置索引
prod_df["万元"] = (prod_df["总金额"] / 10000).round(1) # 转换为万元

# 按渠道汇总
chan_df = (df.groupby("渠道")["销售金额"]              # 按渠道分组
           .sum()                                      # 求和
           .sort_values(ascending=False))              # 降序排列


# ── 4-1 月度销售趋势折线图 ──────────────────────────────────
print("── 4-1 月度销售趋势图 ──")

fig, ax = plt.subplots(figsize=(12, 6))               # 创建宽幅画布

xi = range(len(monthly_df))                            # x 轴整数位置（确保柱间距均匀）
ax.fill_between(xi, monthly_df["万元"],                # 折线下方面积填充
                alpha=0.12, color="#4C72B0")           # 低透明度蓝色填充

ax.plot(xi, monthly_df["万元"],                        # 绘制月度销售额折线
        color="#4C72B0", linewidth=2.5,               # 颜色和线宽
        marker="o", markersize=9,                     # 圆形标记，大小 9
        markerfacecolor="white",                       # 标记内部白色（空心效果）
        markeredgecolor="#4C72B0", markeredgewidth=2,  # 标记边框颜色和宽度
        zorder=3)                                      # 渲染在填充区域上层

for i, row in monthly_df.iterrows():                   # 遍历每月，在点上方标注数值
    ax.text(i, row["万元"] + 1.8,                      # 文字位置：x=月份位置，y=点上方
            f"{row['万元']}万",                        # 文字内容：金额+单位
            ha="center", fontsize=9, color="#333")    # 水平居中，深灰色

# 标注最高峰值
pk = int(monthly_df["万元"].idxmax())                  # 最大值所在行的整数索引
ax.annotate(f"峰值\n{monthly_df.loc[pk,'万元']}万",   # 注释文字（\n 换行）
            xy=(pk, monthly_df.loc[pk, "万元"]),       # 箭头指向峰值点
            xytext=(pk + 0.4, monthly_df.loc[pk, "万元"] + 10),  # 文字偏移位置
            arrowprops=dict(arrowstyle="->", color="red", lw=1.5),  # 红色箭头
            fontsize=10, color="red", fontweight="bold")  # 红色加粗

ax.axhline(monthly_df["万元"].mean(),                  # 绘制月均值水平参考线
           color="orange", linewidth=1.5,              # 橙色
           linestyle=":", alpha=0.9,                   # 点线，高不透明度
           label=f"月均 {monthly_df['万元'].mean():.1f}万")  # 图例标签

ax.set_xticks(list(xi))                               # 设置 x 刻度位置
ax.set_xticklabels(monthly_df["标签"].tolist(),       # 设置 x 刻度为中文月份标签
                   fontsize=10)
ax.set_title("2024年月度销售额趋势",                   # 标题
             fontsize=15, fontweight="bold", pad=15)   # 加粗，顶部间距
ax.set_xlabel("月份", fontsize=12)                    # x 轴标签
ax.set_ylabel("销售额（万元）", fontsize=12)          # y 轴标签
ax.legend(fontsize=11, loc="upper left")              # 图例
ax.set_ylim(0, monthly_df["万元"].max() * 1.3)        # y 轴上限留 30% 空间
ax.grid(axis="y", alpha=0.3, linestyle="--")          # 水平网格线

fig.tight_layout()                                    # 调整布局
fig.savefig(OUT / "08_monthly_trend.png", dpi=150)   # 保存 PNG（150 DPI）
plt.close(fig)                                        # 关闭释放内存
print(f"  已保存：{OUT}/08_monthly_trend.png")


# ── 4-2 产品销量柱状图 ──────────────────────────────────────
print("── 4-2 产品销量柱状图 ──")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))       # 1 行 2 列：左销售额，右销售数量

bar_palette = ["#4C72B0","#DD8452","#55A868","#C44E52","#8172B3"]  # 五产品各一颜色

# 左图：各产品销售额柱状图
bars_left = axes[0].bar(
    prod_df["产品"],                                   # x 轴：产品名称
    prod_df["万元"],                                   # y 轴：销售额（万元）
    color=bar_palette,                                 # 每根柱使用不同颜色
    alpha=0.88,                                        # 透明度
    edgecolor="white", linewidth=0.8,                  # 白色边框
    width=0.6)                                         # 柱宽（0~1，1 表示占满刻度间隔）

for bar, val in zip(bars_left, prod_df["万元"]):       # 遍历柱子，添加柱顶数值标注
    axes[0].text(bar.get_x() + bar.get_width() / 2,   # 文字 x：柱子水平中心
                 bar.get_height() + 0.5,               # 文字 y：柱顶上方 0.5 单位
                 f"{val}万",                           # 文字内容：金额+单位
                 ha="center", va="bottom", fontsize=10)  # 居中对齐

axes[0].set_title("各产品销售额",                      # 子图标题
                  fontsize=14, fontweight="bold")
axes[0].set_xlabel("产品", fontsize=12)               # x 轴标签
axes[0].set_ylabel("销售额（万元）", fontsize=12)     # y 轴标签
axes[0].set_ylim(0, prod_df["万元"].max() * 1.2)      # 留顶部空间
axes[0].grid(axis="y", alpha=0.3, linestyle="--")     # 水平网格线

# 右图：各产品销售数量水平柱状图（按数量从小到大排，视觉从下往上递增）
qty_sorted = prod_df.sort_values("总数量")             # 水平柱最底部=最小值，顶部=最大值
axes[1].barh(qty_sorted["产品"],                       # y 轴：产品名称（水平柱的类别轴）
             qty_sorted["总数量"],                      # x 轴：销售数量（水平柱的数值轴）
             color=bar_palette[::-1],                  # 颜色列表反转（与左图错开）
             alpha=0.88,                               # 透明度
             edgecolor="white",                        # 边框
             height=0.6)                               # 水平柱的"高度"（即柱的粗细）

for i, (_, row) in enumerate(qty_sorted.iterrows()):  # 遍历每行，在柱右侧添加数值
    axes[1].text(row["总数量"] + 15,                   # 文字 x：柱右端偏右 15 单位
                 i,                                    # 文字 y：对应行索引位置
                 f"{int(row['总数量'])}件",             # 文字内容：整数+件
                 va="center", fontsize=10)             # 垂直居中

axes[1].set_title("各产品销售数量",                    # 子图标题
                  fontsize=14, fontweight="bold")
axes[1].set_xlabel("销售数量（件）", fontsize=12)     # x 轴标签（水平柱 x 是数值）
axes[1].set_ylabel("产品", fontsize=12)               # y 轴标签（水平柱 y 是类别）
axes[1].set_xlim(0, qty_sorted["总数量"].max() * 1.2) # 右侧留空间放数值标注
axes[1].grid(axis="x", alpha=0.3, linestyle="--")    # 垂直网格线（x 方向）

fig.suptitle("产品销售分析",                           # 整张画布总标题
             fontsize=16, fontweight="bold", y=1.02)   # 超出图像顶部
fig.tight_layout()                                    # 调整子图间距
fig.savefig(OUT / "09_product_bar.png",               # 保存 PNG
            bbox_inches="tight", dpi=150)              # 防截断，高分辨率
plt.close(fig)                                        # 关闭
print(f"  已保存：{OUT}/09_product_bar.png")


# ── 4-3 销售额占比饼图 ──────────────────────────────────────
print("── 4-3 销售额占比饼图 ──")

prod_pie_vals = prod_df.set_index("产品")["总金额"]    # 产品 → 总金额 Series（已降序）
chan_colors   = ["#4ECDC4", "#FF6B6B", "#FFA07A"]      # 三渠道颜色：绿/红/橙

fig, axes = plt.subplots(1, 2, figsize=(14, 7))        # 1 行 2 列子图

# 左：产品占比环形图
explode_p = [0.05] + [0] * (len(prod_pie_vals) - 1)   # 突出最大扇区（第一个=销售额最高）
w1, t1, p1 = axes[0].pie(
    prod_pie_vals.values,                              # 各产品销售额（数值越大扇区越大）
    labels=prod_pie_vals.index,                        # 产品名称标签
    explode=explode_p,                                 # 突出偏移量列表
    colors=bar_palette,                                # 五产品颜色
    autopct="%1.1f%%",                                # 百分比（保留 1 位小数）
    pctdistance=0.80,                                  # 百分比文字距圆心 80% 处
    startangle=90,                                     # 从 12 点方向开始
    wedgeprops=dict(edgecolor="white",                # 扇区间白色分隔
                    linewidth=2,                       # 分隔线宽度
                    width=0.55))                       # width=0.55 → 形成环形（55% 宽度）

for item in p1:                                        # 调整百分比文字样式
    item.set_fontsize(10)                              # 字号 10
    item.set_color("white")                            # 白色（在彩色背景上清晰）

axes[0].text(0, 0,                                     # 在环形中央插入文字
             f"总计\n{prod_pie_vals.sum()/10000:.0f}万",  # 显示总销售额（万元）
             ha="center", va="center",                 # 水平垂直居中
             fontsize=13, fontweight="bold",            # 加粗
             color="#333")                             # 深灰色
axes[0].set_title("产品销售额占比",                    # 左图标题
                  fontsize=14, fontweight="bold", pad=20)  # 顶部间距

# 右：渠道占比饼图（包含百分比和金额双行标注）
w2, t2, p2 = axes[1].pie(
    chan_df.values,                                    # 各渠道销售额
    labels=chan_df.index,                              # 渠道名称
    colors=chan_colors,                                # 渠道颜色
    autopct=lambda pct: (                              # 自定义百分比格式（lambda 函数）
        f"{pct:.1f}%\n"                               # 第一行：百分比
        f"({int(pct/100*chan_df.sum()/10000)}万)"),    # 第二行：对应金额（万元）
    pctdistance=0.65,                                  # 百分比文字距圆心 65%（在扇区内）
    startangle=90,                                     # 起始角度
    shadow=True,                                       # 显示阴影
    wedgeprops=dict(edgecolor="white", linewidth=2))   # 白色分隔线

for t in t2:                                           # 调整渠道名称标签
    t.set_fontsize(12)                                 # 字号 12
    t.set_fontweight("bold")                           # 加粗
for p in p2:                                           # 调整百分比文字
    p.set_fontsize(9)                                  # 字号小（因双行内容多）
    p.set_color("white")                               # 白色

axes[1].set_title("渠道销售额占比",                    # 右图标题
                  fontsize=14, fontweight="bold", pad=20)

fig.suptitle("销售额占比分析",                         # 总标题
             fontsize=16, fontweight="bold", y=1.02)   # 标题位于图表上方
fig.tight_layout()                                    # 调整布局
fig.savefig(OUT / "10_pie_analysis.png",              # 保存 PNG
            bbox_inches="tight", dpi=150)              # 防截断，高分辨率
plt.close(fig)                                        # 关闭
print(f"  已保存：{OUT}/10_pie_analysis.png")


# ── 4-4 综合销售看板（GridSpec 大图）────────────────────────
print("── 4-4 综合销售看板 ──")

fig = plt.figure(figsize=(16, 10))                    # 大画布：宽 16 高 10 英寸
gs  = gridspec.GridSpec(2, 3,                          # 2 行 × 3 列网格
                        figure=fig,                    # 绑定画布
                        hspace=0.45,                   # 子图垂直间距
                        wspace=0.35)                   # 子图水平间距

# 顶部跨 3 列：月度趋势折线图
ax_t = fig.add_subplot(gs[0, :])                      # gs[0,:] = 第 0 行全部列
ax_t.fill_between(range(len(monthly_df)), monthly_df["万元"],  # 面积填充
                  alpha=0.12, color="#4C72B0")          # 低透明度
ax_t.plot(range(len(monthly_df)), monthly_df["万元"],  # 月度折线
          color="#4C72B0", linewidth=2.5,              # 蓝色线
          marker="o", markersize=8,                    # 圆形标记
          markerfacecolor="white",                     # 空心效果
          markeredgecolor="#4C72B0", markeredgewidth=2)  # 边框
for i, v in enumerate(monthly_df["万元"]):             # 标注每月数值
    ax_t.text(i, v + 1.5, f"{v}万",                   # 点上方文字
              ha="center", fontsize=8.5, color="#444") # 居中，深灰
ax_t.axhline(monthly_df["万元"].mean(),                # 均值参考线
             color="orange", linewidth=1.5,            # 橙色
             linestyle=":", alpha=0.9,                 # 点线
             label=f"月均{monthly_df['万元'].mean():.0f}万")  # 图例
ax_t.legend(loc="upper left", fontsize=10)             # 图例位置
ax_t.set_xticks(range(len(monthly_df)))               # x 刻度位置
ax_t.set_xticklabels(monthly_df["标签"].tolist(), fontsize=9)  # 月份标签
ax_t.set_title("月度销售额趋势", fontsize=13, fontweight="bold")  # 标题
ax_t.set_ylabel("万元", fontsize=10)                  # y 轴标签
ax_t.set_ylim(0, monthly_df["万元"].max() * 1.35)     # y 轴上限
ax_t.grid(axis="y", alpha=0.3, linestyle="--")        # 水平网格线

# 左下：产品销售额柱状图
ax_b = fig.add_subplot(gs[1, 0])                      # gs[1,0] = 第 1 行第 0 列
ax_b.bar(prod_df["产品"], prod_df["万元"],             # 柱状图
         color=bar_palette, alpha=0.88, edgecolor="white")  # 颜色和透明度
for bar_p in ax_b.patches:                             # patches 属性包含所有柱子矩形对象
    ax_b.text(bar_p.get_x() + bar_p.get_width() / 2,  # 柱子水平中心
              bar_p.get_height() + 0.3,                # 柱顶上方
              f"{bar_p.get_height():.0f}万",           # 柱高数值（万元）
              ha="center", fontsize=8)                 # 居中，字号 8
ax_b.set_title("产品销售额", fontsize=11, fontweight="bold")  # 标题
ax_b.set_ylabel("万元", fontsize=9)                   # y 轴标签
ax_b.tick_params(axis="x", labelsize=8)               # x 刻度字号
ax_b.set_ylim(0, prod_df["万元"].max() * 1.28)        # y 轴上限
ax_b.grid(axis="y", alpha=0.3, linestyle="--")        # 水平网格线

# 中下：渠道占比饼图
ax_p = fig.add_subplot(gs[1, 1])                      # 第 1 行第 1 列
ax_p.pie(chan_df.values,                               # 渠道销售额
         labels=chan_df.index,                         # 渠道名称
         colors=chan_colors,                           # 渠道颜色
         autopct="%1.0f%%",                            # 整数百分比
         startangle=90,                                # 起始角度
         wedgeprops=dict(edgecolor="white", linewidth=1.5),  # 白色边框
         textprops={"fontsize": 9})                    # 标签字号
ax_p.set_title("渠道销售占比", fontsize=11, fontweight="bold")  # 标题

# 右下：大区销售额水平柱状图
ax_r = fig.add_subplot(gs[1, 2])                      # 第 1 行第 2 列
region_s = (df.groupby("大区")["销售金额"]             # 按大区分组
            .sum().div(10000).round(1)                 # 汇总后转换为万元
            .sort_values())                            # 从小到大排列（视觉上由下至上递增）
ax_r.barh(region_s.index, region_s.values,             # 水平柱：y=大区，x=销售额
          color=bar_palette, alpha=0.88,               # 颜色和透明度
          edgecolor="white", height=0.6)               # 边框和柱高
for i, (reg, val) in enumerate(region_s.items()):      # 在柱右侧标注数值
    ax_r.text(val + 0.3, i, f"{val}万",               # 文字位置（柱右侧偏移）
              va="center", fontsize=9)                 # 垂直居中
ax_r.set_title("大区销售额", fontsize=11, fontweight="bold")  # 标题
ax_r.set_xlabel("万元", fontsize=9)                   # x 轴标签（水平柱 x=数值）
ax_r.set_xlim(0, region_s.max() * 1.28)               # 右侧留标注空间
ax_r.grid(axis="x", alpha=0.3, linestyle="--")        # x 方向网格线

fig.suptitle("2024年销售综合看板",                     # 整张画布大标题
             fontsize=18, fontweight="bold", y=1.01)   # 标题在图表上方

fig.savefig(OUT / "11_sales_dashboard.png",            # 保存综合看板 PNG
            bbox_inches="tight", dpi=150)               # 防截断，高分辨率
plt.close(fig)                                         # 关闭释放内存
print(f"  已保存：{OUT}/11_sales_dashboard.png")


# ============================================================
# 汇总与清理
# ============================================================
print("\n══ 图像文件汇总 ══")
png_files = sorted(OUT.glob("*.png"))                  # 获取所有 PNG（按文件名排序）
total_kb  = sum(f.stat().st_size for f in png_files) / 1024  # 计算总大小（KB）
for f in png_files:                                    # 遍历每个文件
    kb = f.stat().st_size / 1024                       # 当前文件大小（KB）
    print(f"  {f.name:<35} {kb:>6.1f} KB")            # 对齐输出文件名和大小
print(f"  共 {len(png_files)} 个文件，总大小 {total_kb:.1f} KB")  # 汇总统计行

shutil.rmtree(OUT)                                     # 删除临时目录及其中所有 PNG 文件
print(f"\n已清理：{OUT}/")                             # 提示清理完成
