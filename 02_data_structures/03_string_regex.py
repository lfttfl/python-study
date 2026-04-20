# Python 数据结构练习：字符串处理与正则表达式
# =====================================================

import re                                     # 导入标准库 re（regular expression）

# ══════════════════════════════════════════════════════
# 一、字符串格式化
# ══════════════════════════════════════════════════════

# ── 1-1 f-string（Python 3.6+，最推荐的写法）─────────

print("── f-string ──")

name  = "小明"
age   = 18
score = 92.5678

# f-string：在字符串前加 f，花括号 {} 内直接写变量或表达式
print(f"姓名：{name}，年龄：{age}")            # 最基础用法

# 花括号内可以写任意表达式，Python 会先求值再插入
print(f"明年 {age + 1} 岁")                   # 表达式：18+1=19
print(f"成绩：{score:.2f}")                    # :.2f 保留两位小数 → 92.57
print(f"成绩：{score:.0f}")                    # :.0f 四舍五入到整数 → 93
print(f"科学计数法：{123456789:.2e}")          # :.2e 科学计数法 → 1.23e+08
print(f"百分比：{0.856:.1%}")                  # :.1% 转百分比，保留1位小数 → 85.6%
print(f"整数位数：{42:05d}")                   # :05d 用 0 填充到宽度 5 → 00042
print(f"逗号分隔千位：{1234567:,}")            # :, 千位分隔符 → 1,234,567

# 对齐控制：< 左对齐  > 右对齐  ^ 居中对齐，数字是总宽度
print(f"{'左对齐':<10}|")                      # 左对齐，宽度10，不足补空格
print(f"{'右对齐':>10}|")                      # 右对齐，宽度10
print(f"{'居中':^10}|")                        # 居中，宽度10
print(f"{'填充':*^10}|")                       # 居中，用 * 填充空白

# 调试用法（Python 3.8+）：变量名=值，方便打印调试信息
x = 42
print(f"{x=}")                                 # 输出 x=42（自动显示变量名和值）
print(f"{score=:.2f}")                         # score=92.57（可以附加格式说明符）

# ── 1-2 str.format()（Python 3.0+，兼容性好）─────────

print("\n── str.format() ──")

# 基础用法：{} 按顺序填入 format() 的参数
print("{}年{}月{}日".format(2024, 4, 20))      # 2024年4月20日

# 按索引填入：{0} {1} 可以复用或乱序
print("{0}喜欢{1}，{1}也喜欢{0}".format("小明", "Python"))

# 按名称填入：更可读，参数顺序无所谓
print("{name}，{age}岁".format(name="小红", age=17))

# 用字典解包传参（** 把字典展开为关键字参数）
info = {"product": "键盘", "price": 299.0, "stock": 50}
print("{product} 售价 {price:.1f} 元，库存 {stock} 件".format(**info))

# format() 同样支持格式说明符
print("{:>10.2f}".format(3.14159))             # 右对齐，宽度10，保留2位小数
print("{:0>8b}".format(42))                    # 42 转二进制，宽度8，左侧补0 → 00101010

# ── 1-3 对齐填充：制表输出 ───────────────────────────

print("\n── 对齐填充：制表输出 ──")

# 用格式化制作整齐的表格（等宽字体下效果最好）
header = f"{'商品':<8}{'单价':>8}{'数量':>6}{'小计':>10}"
sep    = "-" * 34                              # 分隔线，长度与表头一致
print(header)
print(sep)

items = [("苹果", 5.5, 10), ("香蕉", 3.2, 5), ("橙子", 4.8, 8)]
for product, price, qty in items:             # 解包元组
    subtotal = price * qty
    print(f"{product:<8}{price:>8.1f}{qty:>6}{subtotal:>10.2f}")  # 统一对齐
print(sep)
total = sum(p * q for _, p, q in items)       # 生成器求总计
print(f"{'合计':<8}{'':>14}{total:>10.2f}")   # 空字符串占位保持对齐

# ── 1-4 旧式 % 格式化（了解即可，遗留代码中常见）────

print("\n── % 格式化（了解）──")

print("姓名：%s，年龄：%d，分数：%.1f" % ("小刚", 19, 88.5))  # %s字符串 %d整数 %f浮点

# ══════════════════════════════════════════════════════
# 二、常用字符串方法
# ══════════════════════════════════════════════════════

print("\n══ 常用字符串方法 ══")

# ── 2-1 查找类方法 ─────────────────────────────────────

text = "Python is great, Python is fun, Python rules!"

# find(子串, start, end)：返回第一次出现的起始索引，找不到返回 -1（不报错）
print(text.find("Python"))                     # 0（第一次在索引 0）
print(text.find("Python", 1))                  # 17（从索引 1 之后找）
print(text.find("Java"))                       # -1（找不到）

# rfind()：从右往左找，返回最后一次出现的索引
print(text.rfind("Python"))                    # 32（最后一次出现）

# index()：与 find 类似，但找不到时抛出 ValueError（需 try-except 保护）
print(text.index("is"))                        # 7

# count(子串)：统计子串出现次数（不重叠计数）
print(text.count("Python"))                    # 3
print(text.count("is"))                        # 2

# startswith(前缀) / endswith(后缀)：检查开头/结尾，返回布尔值
print(text.startswith("Python"))               # True
print(text.endswith("!"))                      # True
print(text.startswith("Java"))                 # False

# 参数可以是元组：检查是否以其中任一字符串开头/结尾
filename = "report_2024.xlsx"
print(filename.endswith((".xlsx", ".xls", ".csv")))   # True（是 Excel 文件）

# ── 2-2 分割与合并 ─────────────────────────────────────

print("\n── 分割与合并 ──")

csv_line = "小明,18,北京,Python"

# split(分隔符, 最大分割次数)：按分隔符切割，返回列表
parts = csv_line.split(",")                    # 按逗号切割
print("split：", parts)                        # ['小明', '18', '北京', 'Python']

parts2 = csv_line.split(",", 2)               # 最多切 2 次，剩余部分保持原样
print("split(maxsplit=2)：", parts2)           # ['小明', '18', '北京,Python']

# rsplit()：从右往左切，限制次数时结果不同
print("rsplit(maxsplit=1)：", csv_line.rsplit(",", 1))  # ['小明,18,北京', 'Python']

# splitlines()：按行分割（支持 \n \r\n \r 等多种换行符）
multi = "第一行\n第二行\r\n第三行"
print("splitlines：", multi.splitlines())      # ['第一行', '第二行', '第三行']

# join(可迭代对象)：用字符串把列表元素拼接成一个字符串
# 注意：join 是字符串方法，调用者是分隔符，参数是要拼接的序列
words = ["Hello", "World", "Python"]
print("-".join(words))                         # Hello-World-Python
print(" ".join(words))                         # Hello World Python
print("".join(words))                          # HelloWorldPython（无分隔符）
print("\n".join(words))                        # 每个单词占一行

# join 比 + 循环拼接效率高：+ 每次创建新字符串，join 一次性分配内存
chars = list("abcde")
print("".join(chars))                          # abcde

# ── 2-3 大小写与空白处理 ──────────────────────────────

print("\n── 大小写与空白 ──")

s = "  Hello World Python  "

print(s.strip())                               # 去掉两端空白（包含\n\t）
print(s.lstrip())                              # 只去左端
print(s.rstrip())                              # 只去右端
print(s.strip().lower())                       # 去空白后转小写
print(s.strip().upper())                       # 去空白后转大写
print("hello world".title())                  # 每个单词首字母大写 → Hello World
print("Hello World".swapcase())               # 大小写互换 → hELLO wORLD
print("hello world".capitalize())             # 只有第一个字符大写 → Hello world

# 检查字符串内容
print("abc123".isalnum())                      # True：全是字母或数字
print("abc".isalpha())                         # True：全是字母
print("123".isdigit())                         # True：全是数字
print("  \t\n".isspace())                      # True：全是空白字符
print("Hello World".istitle())                 # True：标题格式

# ── 2-4 替换与编辑 ────────────────────────────────────

print("\n── 替换 ──")

sentence = "I like cats, cats are cute, cats are fun"
print(sentence.replace("cats", "dogs"))        # 替换所有
print(sentence.replace("cats", "dogs", 1))    # 只替换第一个（count 参数）

# str.maketrans + translate：批量字符替换（比多次 replace 高效）
table = str.maketrans("aeiou", "AEIOU")       # 建立字符映射表：小写元音→大写
print("hello world".translate(table))         # hEllO wOrld

# removeprefix / removesuffix（Python 3.9+）
filename2 = "report_final.xlsx"
print(filename2.removeprefix("report_"))       # final.xlsx（只删前缀，不存在则不变）
print(filename2.removesuffix(".xlsx"))         # report_final

# center / ljust / rjust：对齐填充的字符串方法版本
print("Python".center(20, "="))               # =======Python=======
print("Python".ljust(20, "-"))                # Python--------------
print("Python".rjust(20, "-"))                # --------------Python
print(str(42).zfill(6))                       # 000042（zero-fill，数字补零专用）

# ══════════════════════════════════════════════════════
# 三、正则表达式基础
# ══════════════════════════════════════════════════════

print("\n══ 正则表达式 ══")

# 正则表达式（regex）：描述字符串模式的"迷你语言"
# re 模块提供所有功能，建议在模式字符串前加 r（raw string）避免反斜杠歧义

# ── 常用元字符速查 ────────────────────────────────────
# .    任意单个字符（除换行）
# \d   任意数字（等价 [0-9]）
# \D   非数字
# \w   字母、数字、下划线（[a-zA-Z0-9_]）
# \W   非 \w
# \s   空白字符（空格、\t、\n 等）
# \S   非空白
# ^    字符串开头（或 [^] 中表示"非"）
# $    字符串结尾
# *    前一项重复 0 次或多次（贪婪）
# +    前一项重复 1 次或多次（贪婪）
# ?    前一项重复 0 次或 1 次（或使贪婪变非贪婪）
# {n}  前一项重复恰好 n 次
# {n,m}前一项重复 n 到 m 次
# []   字符集，匹配其中任一字符
# ()   捕获组，把匹配的子串单独提取出来
# |    或，匹配左边或右边
# (?:) 非捕获组，分组但不提取

# ── 3-1 re.match()：从字符串开头匹配 ─────────────────

print("\n── re.match() ──")

# match() 只从字符串的起始位置开始尝试匹配，返回 Match 对象或 None
pattern = r"\d+"                              # \d+ 匹配一个或多个数字
m = re.match(pattern, "123abc")              # 字符串以数字开头，匹配成功
print(m)                                      # <re.Match object>
print(m.group())                              # "123"，group() 返回完整匹配内容
print(m.start(), m.end())                     # 0 3，匹配的起止索引（不含 end）
print(m.span())                               # (0, 3)，等价 (start, end)

no_match = re.match(pattern, "abc123")        # 字符串以字母开头，从头匹配失败
print(no_match)                               # None

# 实际使用时必须先判断是否为 None，避免 AttributeError
if m:                                         # Match 对象是真值，None 是假值
    print("匹配成功：", m.group())

# ── 3-2 re.search()：全文扫描，找第一个匹配 ──────────

print("\n── re.search() ──")

# search() 扫描整个字符串，找到第一个匹配就返回，找不到返回 None
text2 = "订单号：ORD-2024-0420，总金额 ¥1,299.00"
m2 = re.search(r"\d+", text2)                # 找第一个数字串
print(m2.group())                             # "2024"（第一个出现的数字串）

# 捕获组：用 () 包裹，用 group(编号) 取出
m3 = re.search(r"ORD-(\d{4})-(\d{4})", text2)   # 两个捕获组
print(m3.group())                             # "ORD-2024-0420"（整体匹配）
print(m3.group(1))                            # "2024"（第1组）
print(m3.group(2))                            # "0420"（第2组）
print(m3.groups())                            # ('2024', '0420')，所有组组成元组

# 命名捕获组 (?P<名称>)：用名称取值，比编号更可读
m4 = re.search(r"ORD-(?P<year>\d{4})-(?P<day>\d{4})", text2)
print(m4.group("year"))                       # "2024"
print(m4.group("day"))                        # "0420"
print(m4.groupdict())                         # {'year': '2024', 'day': '0420'}

# ── 3-3 re.findall()：返回所有匹配 ────────────────────

print("\n── re.findall() ──")

# findall() 返回所有非重叠匹配的列表；有捕获组时返回组内容
numbers_text = "苹果3个，香蕉12个，橙子5个，葡萄100个"

# 无捕获组：返回匹配字符串列表
nums = re.findall(r"\d+", numbers_text)
print("所有数字：", nums)                      # ['3', '12', '5', '100']

# 有一个捕获组：返回组内容的列表
pairs = re.findall(r"(\w+?)\d+", numbers_text)  # 非贪婪匹配水果名
print("水果名：", pairs)                       # 取决于具体匹配，演示捕获组

# 有多个捕获组：返回元组列表
log = "2024-04-20 ERROR: disk full; 2024-04-21 INFO: backup done"
entries = re.findall(r"(\d{4}-\d{2}-\d{2}) (\w+): (.+?)(?:;|$)", log)
print("日志解析：")
for date, level, msg in entries:              # 解包每个匹配的三个组
    print(f"  [{level}] {date} → {msg.strip()}")

# ── 3-4 re.finditer()：返回迭代器（省内存）───────────

print("\n── re.finditer() ──")

# finditer() 与 findall() 类似，但返回迭代器（逐个产出 Match 对象），适合大文本
text3 = "联系我：13812345678 或 021-88889999 或 400-800-1234"
for m in re.finditer(r"\d[\d-]{6,}", text3):  # 以数字开头，含数字和短横线，长度>=7
    print(f"  找到 '{m.group()}' 在位置 {m.start()}-{m.end()}")

# ── 3-5 re.sub()：替换 ────────────────────────────────

print("\n── re.sub() ──")

# sub(模式, 替换内容, 字符串, count=0)：把所有匹配替换为指定内容
# count=0 表示替换全部，count=n 只替换前 n 个

dirty = "  Python   is    great  "
clean = re.sub(r"\s+", " ", dirty.strip())    # 把连续空白替换为单个空格
print("去多余空格：", clean)                   # "Python is great"

# 替换内容可以引用捕获组：\1 表示第1组，\2 表示第2组
date_str = "2024/04/20"
formatted = re.sub(r"(\d{4})/(\d{2})/(\d{2})", r"\1-\2-\3", date_str)
print("日期格式化：", formatted)               # "2024-04-20"

# 替换内容可以是函数：每次匹配都调用该函数，返回值作为替换字符串
def double_num(match):                        # 参数是 Match 对象
    return str(int(match.group()) * 2)        # 把匹配到的数字乘以 2

result = re.sub(r"\d+", double_num, "苹果3个，香蕉12个")
print("数字翻倍：", result)                    # "苹果6个，香蕉24个"

# subn()：与 sub 相同，但返回 (新字符串, 替换次数) 元组
new_str, count_replaced = re.subn(r"\d+", "X", "a1b22c333")
print(f"subn：'{new_str}'，共替换 {count_replaced} 处")

# ── 3-6 re.compile()：预编译模式（提升重复使用的性能）──

print("\n── re.compile() ──")

# 如果同一模式要多次使用，先 compile() 生成正则对象，避免重复解析
phone_re = re.compile(r"1[3-9]\d{9}")         # 预编译手机号模式

texts = ["联系：13812345678", "电话：2888888", "手机：15900001234"]
for t in texts:
    m = phone_re.search(t)                    # 直接调用对象的方法，不用重传模式
    print(f"  '{t}' → {'找到: ' + m.group() if m else '未找到'}")

# compile 对象支持所有 re 函数的同名方法：match search findall sub 等
digits_re = re.compile(r"\d+")
print(digits_re.findall("abc123def456"))      # ['123', '456']

# ── 3-7 常用标志（flags）────────────────────────────────

print("\n── 常用 flags ──")

# re.IGNORECASE / re.I：忽略大小写
print(re.findall(r"python", "Python PYTHON python", re.I))  # ['Python', 'PYTHON', 'python']

# re.MULTILINE / re.M：^ 和 $ 匹配每一行的开头/结尾，而非整个字符串
multi_text = "first\nsecond\nthird"
print(re.findall(r"^\w+", multi_text, re.M))   # ['first', 'second', 'third']

# re.DOTALL / re.S：让 . 也匹配换行符
html = "<div>\nhello\n</div>"
m5 = re.search(r"<div>(.+?)</div>", html, re.S)  # 不加 re.S 则 . 不跨行
print("跨行匹配：", m5.group(1).strip() if m5 else "未匹配")

# 多个标志用 | 组合
print(re.findall(r"^python", "Python\npython", re.I | re.M))

# ══════════════════════════════════════════════════════
# 四、实战场景：提取手机号、邮箱、金额
# ══════════════════════════════════════════════════════

print("\n══ 实战：信息提取 ══")

# 真实场景中的混合文本（模拟客服聊天记录）
raw_text = """
客户A：您好，我的手机号是 13812345678，请给我发验证码。
客服：好的，请问您的邮箱是？
客户A：是 alice@example.com，另外发一份到 alice.work@company.org 也行。
客服：收到，您这笔订单金额是 ¥1,299.00，另有运费 ¥15.5，合计 ¥1314.50。
客户B：我的联系方式是 18600001234 或者 021-55556666（固话）。
客户B：邮件发 bob123@mail.cn，金额不对，应该是 ¥999 不是 ¥1,000.00。
"""

# ── 4-1 提取手机号 ────────────────────────────────────

print("── 提取手机号 ──")

# 中国手机号规则：1开头，第二位3-9，后面9位数字，共11位
# 需要排除固话：用 (?<!\d) 前向否定断言（前面不能是数字）避免提取固话中间的数字
phone_pattern = re.compile(
    r"(?<!\d)"           # 前面不能紧跟数字（负向后顾断言，避免匹配固话中的数字）
    r"1[3-9]\d{9}"       # 手机号主体：1开头，第2位3-9，再9位数字
    r"(?!\d)"            # 后面不能紧跟数字（负向先行断言）
)
phones = phone_pattern.findall(raw_text)
print("手机号：", phones)                      # ['13812345678', '18600001234']

# ── 4-2 提取邮箱地址 ──────────────────────────────────

print("\n── 提取邮箱 ──")

# 邮箱规则：用户名@域名.顶级域名
# 用户名：字母/数字/点/加号/短横线，1个以上
# 域名：字母/数字/短横线，1个以上
# 顶级域名：字母，2-6位（com org cn 等）
email_pattern = re.compile(
    r"[a-zA-Z0-9._%+\-]+"    # 用户名：允许字母数字和特殊字符
    r"@"                       # @ 符号
    r"[a-zA-Z0-9\-]+"         # 域名主体
    r"(?:\.[a-zA-Z0-9\-]+)*"  # 可选子域名（如 mail.sub）
    r"\.[a-zA-Z]{2,6}"        # 顶级域名（.com .org .cn 等）
)
emails = email_pattern.findall(raw_text)
print("邮箱：", emails)      # ['alice@example.com', 'alice.work@company.org', 'bob123@mail.cn']

# ── 4-3 提取金额 ──────────────────────────────────────

print("\n── 提取金额 ──")

# 金额规则：¥ 符号后跟数字，数字可含千位逗号和小数点
# ¥1,299.00  ¥15.5  ¥999
amount_pattern = re.compile(
    r"¥"                             # 人民币符号（¥ 是 Unicode 字符）
    r"("                             # 捕获组开始
    r"(?:\d{1,3}(?:,\d{3})+"        # 分支1：带千位逗号（1,299 / 1,000,000）
    r"|\d+)"                         # 分支2：不带逗号的任意位数整数（1314 / 999）
    r"(?:\.\d+)?)"                   # 小数部分（.数字），0次或1次，捕获组结束
)
# 返回捕获组内容（不含 ¥ 符号），便于后续转为数字
amount_strs = amount_pattern.findall(raw_text)
print("金额字符串：", amount_strs)             # ['1,299.00', '15.5', '1314.50', '999', '1,000.00']

# 把提取的金额字符串转换为浮点数（去掉千位逗号）
amounts = [float(a.replace(",", "")) for a in amount_strs]
print("金额数值：", amounts)                   # [1299.0, 15.5, 1314.5, 999.0, 1000.0]
print(f"最大金额：¥{max(amounts):,.2f}")       # ¥1,314.50（:, 加千位分隔符）
print(f"金额合计：¥{sum(amounts):,.2f}")

# ── 4-4 综合：结构化解析联系人 ───────────────────────

print("\n── 综合：解析联系人 ──")

# 用命名捕获组，一次解析多个字段，结果整理成字典列表
contacts_text = """
张三：13900001111，zhangsan@qq.com，余额¥500
李四：18700002222，lisi@163.com，余额¥1,200.50
"""

# 模式：捕获姓名、手机、邮箱、余额四个字段
contact_re = re.compile(
    r"(?P<name>[\u4e00-\u9fff]+)"          # 姓名：Unicode 中文字符范围
    r"："                                   # 中文冒号
    r"(?P<phone>1[3-9]\d{9})"             # 手机号
    r"，"                                   # 中文逗号分隔
    r"(?P<email>[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,6})"  # 邮箱
    r"，余额¥"                              # 固定文字
    r"(?P<balance>[\d,]+\.?\d*)"           # 余额（含千位逗号和可选小数）
)

contacts = []
for m in contact_re.finditer(contacts_text):
    d = m.groupdict()                       # 转为字典：{'name': ..., 'phone': ..., ...}
    d["balance"] = float(d["balance"].replace(",", ""))  # 余额转浮点
    contacts.append(d)

print(f"{'姓名':<6}{'手机':<14}{'邮箱':<22}{'余额':>10}")
print("-" * 54)
for c in contacts:
    print(f"{c['name']:<6}{c['phone']:<14}{c['email']:<22}{c['balance']:>10,.2f}")
