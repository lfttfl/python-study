# Python 基础练习：条件判断与循环
# =====================================================

# ── 一、if / elif / else 条件判断 ──────────────────────

score = 85                        # 定义一个成绩变量

# if 是"如果"，条件为 True 时执行缩进块内的代码
if score >= 90:                   # 条件：分数 >= 90
    print("优秀")                 # 条件成立时执行

# elif 是"否则如果"，前面的 if 不成立才会判断 elif
elif score >= 75:                 # 条件：75 <= 分数 < 90
    print("良好")                 # 输出：良好

# else 是"否则"，上面所有条件都不成立时执行
else:                             # 分数 < 75
    print("需要加油")

# 条件可以用 and（且）、or（或）、not（非）组合
age = 20                          # 年龄
has_id = True                     # 是否持有证件

if age >= 18 and has_id:          # 两个条件都必须为 True
    print("可以入场")

# 比较运算符：== 等于  != 不等于  >  <  >=  <=
x = 10
if x != 5:                        # x 不等于 5，条件为 True
    print(f"x 的值是 {x}，不是 5")

# 三元表达式（单行 if-else）：值A if 条件 else 值B
label = "偶数" if x % 2 == 0 else "奇数"   # % 是取余运算
print(f"{x} 是 {label}")          # 输出：10 是 偶数

# ── 二、for 循环 + range() ────────────────────────────

print("\n── for 循环 ──")

# for 循环：依次取出序列中每个元素，赋给变量后执行循环体
fruits = ["苹果", "香蕉", "橙子"]  # 列表（序列的一种）
for fruit in fruits:              # fruit 每次取列表中的下一个元素
    print(f"水果：{fruit}")       # 循环体，缩进表示属于 for 块

# range(n) 生成 0, 1, 2, ..., n-1 的整数序列（不包含 n）
for i in range(5):                # i 依次为 0 1 2 3 4
    print(i, end=" ")             # end=" " 让 print 不换行，用空格结尾
print()                           # 换行，保持输出整洁

# range(start, stop) 生成 start 到 stop-1 的序列
for i in range(1, 6):             # i 依次为 1 2 3 4 5
    print(i, end=" ")
print()

# range(start, stop, step) 第三个参数是步长（间隔）
for i in range(0, 10, 2):        # i 依次为 0 2 4 6 8，每次加 2
    print(i, end=" ")
print()

# enumerate() 同时获取索引和值，避免手动维护计数器
for index, fruit in enumerate(fruits):       # index 从 0 开始
    print(f"第{index}个：{fruit}")

# enumerate(seq, start=1) 让索引从 1 开始
for index, fruit in enumerate(fruits, start=1):
    print(f"第{index}个：{fruit}")

# 嵌套 for 循环：循环里面再套循环，外层每走一步内层走完整圈
print("\n九九乘法表（前三行）：")
for row in range(1, 4):           # 外层控制行（1 到 3）
    for col in range(1, row + 1): # 内层控制列（1 到当前行号）
        print(f"{col}×{row}={col*row}", end="  ")  # 横向打印
    print()                       # 内层结束后换行

# ── 三、while 循环 ────────────────────────────────────

print("\n── while 循环 ──")

# while 条件为 True 时反复执行循环体，直到条件变 False
count = 0                         # 初始化计数器
while count < 5:                  # 只要 count 小于 5 就继续循环
    print(f"count = {count}")     # 输出当前值
    count += 1                    # count = count + 1，每次加 1，防止死循环

# while 常用于"不知道循环几次"的场景，比如等待用户输入
# （此处用变量模拟，避免真正的交互式输入）
total = 0                         # 累加器
num = 1                           # 从 1 开始累加
while num <= 100:                 # 计算 1 + 2 + ... + 100
    total += num                  # 把当前数加进总和
    num += 1                      # 准备下一个数
print(f"1到100的总和 = {total}")  # 高斯公式结果 5050

# ── 四、break / continue / pass ───────────────────────

print("\n── break ──")

# break：立刻退出整个循环，不再执行后续迭代
for i in range(10):               # 本来要循环 0 到 9
    if i == 5:                    # 当 i 等于 5 时
        break                     # 跳出循环，循环立即终止
    print(i, end=" ")             # 只会输出 0 1 2 3 4
print()                           # 换行

# while + break 常用于"找到目标就停"的搜索模式
target = 7
n = 0
while True:                       # 无限循环，必须靠 break 退出
    if n == target:               # 找到目标
        print(f"找到了：{n}")
        break                     # 退出循环
    n += 1                        # 继续找下一个

print("\n── continue ──")

# continue：跳过本次迭代剩余代码，直接进入下一次循环
for i in range(10):               # 循环 0 到 9
    if i % 2 == 0:                # 如果是偶数（余数为 0）
        continue                  # 跳过下面的 print，直接进下一轮
    print(i, end=" ")             # 只打印奇数：1 3 5 7 9
print()

# continue 常用于"过滤不符合条件的元素"
print("\n── pass ──")

# pass：什么都不做的占位符，语法上需要有代码块但逻辑暂未实现时使用
for i in range(3):
    if i == 1:
        pass                      # 暂时跳过对 i==1 的处理，不报错
    else:
        print(f"处理 i = {i}")

# pass 也常用于定义空函数或空类，先占位后填充
def todo_function():
    pass                          # 函数体不能为空，用 pass 占位

# ── 综合示例：猜数字逻辑 ──────────────────────────────

print("\n── 综合示例：模拟猜数字 ──")

secret = 42                       # 预设的"正确答案"
guesses = [10, 55, 42, 80]       # 模拟用户依次猜的数字

for attempt, guess in enumerate(guesses, start=1):  # 记录第几次
    if guess < secret:            # 猜小了
        print(f"第{attempt}次猜 {guess}：太小了")
    elif guess > secret:          # 猜大了
        print(f"第{attempt}次猜 {guess}：太大了")
    else:                         # 猜对了
        print(f"第{attempt}次猜 {guess}：恭喜猜对！")
        break                     # 猜对了立刻退出，不再继续
else:                             # for-else：循环正常结束（没有 break）时执行
    print("所有猜测用完，未能猜中")  # 本例中不会到达这里
