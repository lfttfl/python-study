# Python 文件 I/O 练习：CSV、JSON 与异常处理
# =====================================================

import csv                                    # 标准库：读写 CSV 格式文件
import json                                   # 标准库：读写 JSON 格式数据
import os
from pathlib import Path
from datetime import datetime, date           # 处理日期时间类型（JSON 序列化需特殊处理）
from decimal import Decimal                   # 高精度小数（同样需要特殊 JSON 序列化）

WORK_DIR = Path(__file__).parent / "tmp_csv_json"   # 所有练习文件放到临时目录
WORK_DIR.mkdir(exist_ok=True)

# ══════════════════════════════════════════════════════
# 一、CSV 文件读写
# ══════════════════════════════════════════════════════

print("══ 一、CSV 读写 ══")

# CSV（Comma-Separated Values）：用逗号（或其他分隔符）分隔字段的纯文本格式
# 每行一条记录，第一行通常是表头
# Python csv 模块自动处理：字段含逗号时加引号、引号转义、换行符等边界情况

# ── 1-1 csv.writer：写入 CSV ──────────────────────────

print("\n── csv.writer ──")

students_path = WORK_DIR / "students.csv"

# newline="" 是 csv 模块要求的写法，防止 Windows 上出现多余的空行
# 原因：csv 模块自己管理换行，如果 open() 也转换换行符，会产生 \r\r\n
with open(students_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)                    # 创建 writer 对象，默认逗号分隔

    # writerow()：写入一行（接受列表或元组）
    writer.writerow(["姓名", "年龄", "城市", "成绩"])   # 写表头

    # 数据行：字段含逗号或引号时，csv 模块会自动加引号保护
    writer.writerow(["小明", 18, "北京", 88.5])
    writer.writerow(["小红", 17, "上海", 92.0])
    writer.writerow(["小刚", 19, "北京,朝阳区", 75.5])  # 含逗号，自动加引号
    writer.writerow(['小李', 18, '广州', 91.0])

    # writerows()：一次写入多行（接受二维列表）
    more_data = [
        ["小王", 20, "深圳", 68.0],
        ["小张", 17, "成都", 85.5],
    ]
    writer.writerows(more_data)               # 批量写入，比循环 writerow() 效率略高

print(f"写入 CSV：{students_path.name}")
print("文件内容：")
print(students_path.read_text(encoding="utf-8"))   # 直接打印查看原始文本

# ── 1-2 csv.reader：读取 CSV ──────────────────────────

print("── csv.reader ──")

with open(students_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)                    # 创建 reader 对象，自动处理引号和转义

    header = next(reader)                     # next() 手动取第一行（表头），跳过它
    print(f"表头：{header}")                  # ['姓名', '年龄', '城市', '成绩']

    for row in reader:                        # reader 是迭代器，每次产出一行（字符串列表）
        # 注意：csv.reader 读出的所有字段都是字符串，需要手动类型转换
        name  = row[0]                        # 字符串，不用转换
        age   = int(row[1])                   # 字符串转整数
        city  = row[2]                        # 可能含逗号，csv 模块已正确处理引号
        score = float(row[3])                 # 字符串转浮点数
        print(f"  {name:4s} {age:3d}岁 {city:10s} {score:.1f}分")

# ── 1-3 csv.DictReader：按列名读取（推荐）────────────

print("\n── csv.DictReader ──")

with open(students_path, "r", newline="", encoding="utf-8") as f:
    # DictReader 自动把第一行当表头，每行返回 OrderedDict（Python 3.8+ 是普通 dict）
    reader = csv.DictReader(f)

    print(f"字段名：{reader.fieldnames}")     # 第一行的表头列表（还未读行时自动预读）

    students = []                             # 收集所有行
    for row in reader:                        # 每个 row 是 {列名: 值} 的字典
        row["年龄"]  = int(row["年龄"])       # 原地转换类型（字典值是字符串，需手动转）
        row["成绩"]  = float(row["成绩"])
        students.append(dict(row))            # dict() 把 DictReader 行转为普通字典

# 字典列表用起来非常方便
print(f"读取 {len(students)} 名学生")
for s in students[:3]:                        # 只打印前3条
    print(f"  {s}")

# ── 1-4 csv.DictWriter：按列名写入（推荐）───────────

print("\n── csv.DictWriter ──")

report_path = WORK_DIR / "report.csv"
fieldnames  = ["姓名", "成绩", "等级", "是否及格"]   # 定义输出列顺序

def grade(score):                             # 根据成绩判断等级
    if score >= 90: return "优秀"
    if score >= 75: return "良好"
    if score >= 60: return "及格"
    return "不及格"

with open(report_path, "w", newline="", encoding="utf-8") as f:
    # DictWriter 需要指定 fieldnames（列名顺序），extrasaction="ignore" 忽略字典中多余的键
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")

    writer.writeheader()                      # 自动写入表头行（按 fieldnames 顺序）

    for s in students:
        writer.writerow({                     # 传入字典，键对应列名，顺序无所谓
            "姓名":   s["姓名"],
            "成绩":   s["成绩"],
            "等级":   grade(s["成绩"]),
            "是否及格": "是" if s["成绩"] >= 60 else "否",
        })

print(f"写入报告：{report_path.name}")
print(report_path.read_text(encoding="utf-8"))

# ── 1-5 自定义分隔符和方言 ───────────────────────────

print("── 自定义分隔符 ──")

tsv_path = WORK_DIR / "data.tsv"             # TSV：Tab 分隔值（Excel 友好）
with open(tsv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")    # delimiter 指定分隔符，这里用 Tab
    writer.writerow(["产品", "单价", "库存"])
    writer.writerows([
        ["苹果", 5.5, 100],
        ["香蕉", 3.2, 200],
        ["橙子", 4.8, 150],
    ])

with open(tsv_path, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")    # 读取时也要指定同样的分隔符
    for row in reader:
        print(f"  {row}")

# csv.register_dialect()：注册自定义方言（一组参数的组合），避免每次重复传参
csv.register_dialect(
    "pipe_separated",                         # 方言名称
    delimiter="|",                            # 管道符分隔
    quotechar='"',                            # 引号字符
    quoting=csv.QUOTE_MINIMAL,                # 只在必要时加引号
)
pipe_path = WORK_DIR / "pipe.csv"
with open(pipe_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, dialect="pipe_separated")   # 用方言名代替写参数
    writer.writerow(["字段A", "字段B", "字段C"])
    writer.writerow(["值1", "值|含管道", "值3"])        # 含分隔符的字段会被自动加引号
print("管道分隔文件：", pipe_path.read_text(encoding="utf-8").strip())

# ══════════════════════════════════════════════════════
# 二、JSON 读写
# ══════════════════════════════════════════════════════

print("\n══ 二、JSON 读写 ══")

# JSON（JavaScript Object Notation）：轻量级数据交换格式
# Python 类型 ↔ JSON 类型对应关系：
#   dict      ↔  object  {}
#   list/tuple↔  array   []
#   str       ↔  string  ""
#   int/float ↔  number
#   True/False↔  true/false
#   None      ↔  null

# ── 2-1 json.dumps / json.loads：内存中的序列化 ───────

print("\n── dumps / loads ──")

data = {
    "name":    "小明",
    "age":     18,
    "scores":  [88, 92, 79],
    "active":  True,
    "address": None,
    "info":    {"city": "北京", "zip": "100000"},
}

# json.dumps：Python 对象 → JSON 字符串（序列化/dumps = dump string）
json_str = json.dumps(data)                   # 默认紧凑格式，无缩进
print(f"紧凑格式（{len(json_str)}字符）：{json_str}")

# ensure_ascii=False：允许非 ASCII 字符直接输出（否则中文变成 \uXXXX 转义）
# indent=N：格式化缩进，让 JSON 人类可读
# sort_keys=True：按字典键排序，输出稳定（便于 diff 和版本控制）
pretty_str = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
print(f"\n格式化输出：\n{pretty_str}")

# separators 参数：控制分隔符（紧凑序列化时去掉多余空格）
compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
print(f"\n极紧凑格式：{compact}")

# json.loads：JSON 字符串 → Python 对象（反序列化/loads = load string）
parsed = json.loads(json_str)                 # 字符串反解析为 Python 对象
print(f"\n反序列化后类型：{type(parsed)}")    # <class 'dict'>
print(f"name：{parsed['name']}，age：{parsed['age']}")
print(f"True 仍是 bool：{type(parsed['active'])}")  # bool，不是字符串

# ── 2-2 json.dump / json.load：文件 I/O ──────────────

print("\n── dump / load（文件）──")

json_path = WORK_DIR / "students.json"

# json.dump：把 Python 对象直接序列化写入文件对象
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(                                # dump（没有 s）：写入文件
        students,                             # 要序列化的 Python 对象
        f,                                    # 文件对象
        ensure_ascii=False,                   # 允许直接写入中文
        indent=2,                             # 缩进 2 空格，格式化输出
    )
print(f"写入 JSON：{json_path.name}（{json_path.stat().st_size} 字节）")

# json.load：从文件对象反序列化
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)                     # load（没有 s）：从文件读取并解析

print(f"从 JSON 读回 {len(loaded)} 条记录")
for item in loaded[:2]:                       # 打印前两条
    print(f"  {item}")

# ── 2-3 处理不可序列化的类型 ─────────────────────────

print("\n── 自定义序列化 ──")

# 以下类型 json.dumps 默认不支持，会抛 TypeError：
# datetime、date、Decimal、set、bytes、自定义类实例

bad_data = {
    "now":    datetime.now(),                 # datetime 对象
    "today":  date.today(),                   # date 对象
    "price":  Decimal("19.99"),               # Decimal 高精度小数
    "tags":   {"python", "json"},             # set 集合
}

try:
    json.dumps(bad_data)                      # 会抛出 TypeError
except TypeError as e:
    print(f"默认序列化失败：{e}")

# 方法1：default 参数（函数）——遇到不支持的类型时调用
def custom_serializer(obj):                   # obj 是无法序列化的对象
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()                # 转为 ISO 8601 字符串："2024-04-20T10:00:00"
    if isinstance(obj, Decimal):
        return float(obj)                     # 转为浮点数（注意精度损失）
    if isinstance(obj, set):
        return sorted(obj)                    # 转为有序列表（set 本身无序）
    if isinstance(obj, bytes):
        return obj.hex()                      # 字节转十六进制字符串
    raise TypeError(f"不支持的类型：{type(obj)}")  # 其他类型继续报错

result = json.dumps(bad_data, default=custom_serializer, ensure_ascii=False, indent=2)
print(f"自定义序列化结果：\n{result}")

# 方法2：继承 json.JSONEncoder 类，重写 default 方法
class ExtendedEncoder(json.JSONEncoder):      # 继承内置编码器
    def default(self, obj):                   # 重写 default 方法
        if isinstance(obj, (datetime, date)):
            return {"__type__": "datetime", "value": obj.isoformat()}  # 带类型标记
        if isinstance(obj, Decimal):
            return {"__type__": "decimal", "value": str(obj)}          # 保留精度
        if isinstance(obj, set):
            return {"__type__": "set", "value": sorted(obj)}
        return super().default(obj)           # 其他类型调用父类处理（抛 TypeError）

encoded = json.dumps(bad_data, cls=ExtendedEncoder, ensure_ascii=False, indent=2)
print(f"\nExtendedEncoder 结果：\n{encoded}")

# 方法3（最简单）：在序列化前手动转换
converted = {
    "now":   bad_data["now"].isoformat(),
    "today": bad_data["today"].isoformat(),
    "price": str(bad_data["price"]),          # 保留精度用字符串
    "tags":  sorted(bad_data["tags"]),
}
print(f"\n手动转换后序列化：{json.dumps(converted, ensure_ascii=False)}")

# ── 2-4 object_hook：自定义反序列化 ──────────────────

print("\n── object_hook 自定义反序列化 ──")

json_with_types = '''
{
    "name": "小明",
    "created": {"__type__": "datetime", "value": "2024-04-20T10:00:00"},
    "balance": {"__type__": "decimal",  "value": "1299.99"},
    "tags":    {"__type__": "set",      "value": ["json", "python"]}
}
'''

def extended_decoder(dct):                    # 每解析到一个 JSON 对象（{}）就调用一次
    if "__type__" in dct:                     # 如果有类型标记
        t = dct["__type__"]
        if t == "datetime":
            return datetime.fromisoformat(dct["value"])   # 字符串还原为 datetime
        if t == "decimal":
            return Decimal(dct["value"])                  # 字符串还原为 Decimal
        if t == "set":
            return set(dct["value"])                      # 列表还原为 set
    return dct                                # 普通对象直接返回

decoded = json.loads(json_with_types, object_hook=extended_decoder)
print(f"还原后类型：")
print(f"  name:    {decoded['name']} ({type(decoded['name']).__name__})")
print(f"  created: {decoded['created']} ({type(decoded['created']).__name__})")
print(f"  balance: {decoded['balance']} ({type(decoded['balance']).__name__})")
print(f"  tags:    {decoded['tags']} ({type(decoded['tags']).__name__})")

# ── 2-5 JSON Lines 格式（JSONL）─────────────────────

print("\n── JSON Lines (JSONL) ──")

# JSONL：每行一个独立的 JSON 对象，适合流式处理大数据集
# 无需一次性加载整个文件，可以逐行解析

jsonl_path = WORK_DIR / "events.jsonl"

events = [                                    # 模拟事件日志
    {"ts": "2024-04-20T10:00:01", "event": "login",   "user": "alice"},
    {"ts": "2024-04-20T10:01:15", "event": "purchase", "user": "alice", "amount": 99.9},
    {"ts": "2024-04-20T10:02:33", "event": "logout",  "user": "alice"},
    {"ts": "2024-04-20T10:03:00", "event": "login",   "user": "bob"},
]

# 写入 JSONL：每行一个 json.dumps，手动加 \n
with open(jsonl_path, "w", encoding="utf-8") as f:
    for event in events:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")  # 每条记录一行

# 读取 JSONL：逐行读取，每行 json.loads
print("读取 JSONL：")
with open(jsonl_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:                              # 跳过空行
            record = json.loads(line)         # 每行独立解析
            print(f"  [{record['ts']}] {record['event']:10s} user={record['user']}")

# ══════════════════════════════════════════════════════
# 三、异常处理
# ══════════════════════════════════════════════════════

print("\n══ 三、异常处理 ══")

# ── 3-1 基础 try / except / else / finally ────────────

print("\n── try / except / else / finally ──")

# Python 异常层次结构（常见的）：
#   BaseException
#     ├── SystemExit（sys.exit() 触发）
#     ├── KeyboardInterrupt（Ctrl+C 触发）
#     └── Exception（所有普通异常的基类）
#           ├── ValueError（值不合法）
#           ├── TypeError（类型不匹配）
#           ├── KeyError（字典键不存在）
#           ├── IndexError（列表索引越界）
#           ├── FileNotFoundError（文件不存在）
#           ├── ZeroDivisionError（除以零）
#           ├── AttributeError（对象无该属性）
#           └── ...

def safe_divide(a, b):
    try:                                      # try 块：放可能出错的代码
        result = a / b
    except ZeroDivisionError:                 # 捕获特定异常类型（最精确）
        print("  [except] 捕获到除零错误")
        return None
    except TypeError as e:                    # as e：把异常对象绑定到变量 e
        print(f"  [except] 类型错误：{e}")
        return None
    else:                                     # else 块：try 正常执行（无异常）时运行
        print(f"  [else]   计算成功，结果 = {result}")
        return result
    finally:                                  # finally 块：无论如何都会执行（异常或正常）
        print("  [finally] 清理工作（比如关闭资源）")

print("10 / 2：")
safe_divide(10, 2)

print("\n10 / 0：")
safe_divide(10, 0)

print("\n'a' / 2：")
safe_divide("a", 2)

# ── 3-2 捕获多个异常 ──────────────────────────────────

print("\n── 捕获多个异常 ──")

def parse_age(text):
    try:
        age = int(text)                       # 可能抛 ValueError（非整数）
        if age < 0 or age > 150:
            raise ValueError(f"年龄 {age} 超出合理范围 [0, 150]")  # 手动抛出
        return age
    except (ValueError, OverflowError) as e: # 用元组同时捕获多种异常
        print(f"  解析失败：{e}")
        return None

parse_age("25")                               # 正常
parse_age("abc")                              # ValueError（int 转换失败）
parse_age("-5")                               # ValueError（手动抛出）
parse_age("200")                              # ValueError（手动抛出）

# ── 3-3 异常链与 raise from ────────────────────────────

print("\n── 异常链 ──")

def load_config(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        # raise X from Y：把原始异常 Y 作为 cause 附加到新异常 X
        # 这样调用方既看到高层错误，又能追溯底层原因
        raise RuntimeError(f"配置文件不存在：{path}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"配置文件格式错误：{path}") from e

try:
    load_config("/nonexistent/config.json")
except RuntimeError as e:
    print(f"高层错误：{e}")
    print(f"底层原因：{e.__cause__}")         # 通过 __cause__ 访问原始异常

# ── 3-4 自定义异常类 ──────────────────────────────────

print("\n── 自定义异常 ──")

# 自定义异常只需继承 Exception（或其子类），命名以 Error 或 Exception 结尾
class DataValidationError(Exception):         # 数据校验错误
    """当输入数据不符合业务规则时抛出"""
    def __init__(self, field, value, reason):
        self.field  = field                   # 哪个字段有问题
        self.value  = value                   # 有问题的值
        self.reason = reason                  # 问题原因
        # 调用父类 __init__ 设置 args，让 str(e) 显示有意义的信息
        super().__init__(f"字段 '{field}' 的值 '{value}' 无效：{reason}")

class ScoreOutOfRangeError(DataValidationError):  # 继承自自定义异常（形成层级）
    """成绩超出 0-100 范围"""
    def __init__(self, score):
        super().__init__("成绩", score, f"必须在 0~100 之间，实际为 {score}")
        self.score = score

def validate_student(name, age, score):
    if not name or not name.strip():          # 姓名不能为空
        raise DataValidationError("姓名", name, "不能为空")
    if not (0 <= age <= 150):                 # 年龄范围检查
        raise DataValidationError("年龄", age, "必须在 0~150 之间")
    if not (0 <= score <= 100):              # 成绩范围检查（用更具体的子类）
        raise ScoreOutOfRangeError(score)
    return {"name": name.strip(), "age": age, "score": score}

test_cases = [
    ("小明", 18, 88),                         # 正常
    ("",    18, 88),                          # 空姓名
    ("小红", 200, 92),                        # 年龄超出
    ("小刚", 19, 105),                        # 成绩超出（触发子类异常）
]

for name, age, score in test_cases:
    try:
        result = validate_student(name, age, score)
        print(f"  ✓ 验证通过：{result}")
    except ScoreOutOfRangeError as e:         # 先捕获子类（更具体）
        print(f"  ✗ 成绩错误：{e}（score={e.score}）")
    except DataValidationError as e:          # 再捕获父类（更宽泛）
        print(f"  ✗ 数据错误：{e}（field={e.field}）")

# ── 3-5 上下文管理器与异常 ────────────────────────────

print("\n── contextlib.suppress（静默特定异常）──")

from contextlib import suppress              # 引入 suppress：忽略指定异常类型

fake_path = WORK_DIR / "nonexistent.json"

# suppress：进入 with 块后，如果发生指定的异常类型，直接静默忽略（不报错）
# 等价于 try: ... except FileNotFoundError: pass
with suppress(FileNotFoundError):
    content = fake_path.read_text(encoding="utf-8")
    print("这行不会执行，因为文件不存在")

print("suppress 正常跳过了 FileNotFoundError")  # 代码继续执行，无报错

# ══════════════════════════════════════════════════════
# 四、综合实战：CSV → 统计 → JSON
# ══════════════════════════════════════════════════════

print("\n══ 四、综合实战：CSV → 统计 → JSON ══")

# 生成更完整的测试数据
sales_csv = WORK_DIR / "sales.csv"
sales_data = [
    ["日期",       "销售员", "产品",   "数量", "单价"],
    ["2024-04-01", "小明",  "苹果",   120,   5.5],
    ["2024-04-01", "小红",  "香蕉",   80,    3.2],
    ["2024-04-02", "小明",  "橙子",   60,    4.8],
    ["2024-04-02", "小刚",  "苹果",   200,   5.5],
    ["2024-04-03", "小红",  "葡萄",   50,    12.0],
    ["2024-04-03", "小明",  "苹果",   90,    5.5],
    ["2024-04-03", "小刚",  "香蕉",   150,   3.2],
    ["2024-04-04", "小红",  "橙子",   70,    4.8],
    ["2024-04-04", "小明",  "葡萄",   30,    12.0],
    ["2024-04-05", "小刚",  "苹果",   180,   5.5],
]

with open(sales_csv, "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(sales_data)       # 一行搞定：直接用 writerows 写入嵌套列表

def analyze_sales(csv_path):
    """读取销售 CSV，返回多维度统计字典"""

    records = []                              # 原始记录列表

    # ── Step 1：读取并校验 CSV ──
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                records.append({
                    "date":     row["日期"],
                    "seller":   row["销售员"],
                    "product":  row["产品"],
                    "qty":      int(row["数量"]),       # 可能抛 ValueError
                    "price":    float(row["单价"]),      # 可能抛 ValueError
                    "revenue":  int(row["数量"]) * float(row["单价"]),  # 计算营收
                })
            except (ValueError, KeyError) as e:
                print(f"  [警告] 跳过无效行：{dict(row)}，原因：{e}")

    if not records:                           # 没有有效记录，抛出自定义异常
        raise DataValidationError("文件", csv_path, "没有有效数据行")

    # ── Step 2：按维度聚合 ──
    by_seller  = {}                           # 按销售员聚合
    by_product = {}                           # 按产品聚合
    by_date    = {}                           # 按日期聚合

    for r in records:
        # 按销售员
        s = by_seller.setdefault(r["seller"], {"qty": 0, "revenue": 0.0})
        s["qty"]     += r["qty"]
        s["revenue"] += r["revenue"]

        # 按产品
        p = by_product.setdefault(r["product"], {"qty": 0, "revenue": 0.0})
        p["qty"]     += r["qty"]
        p["revenue"] += r["revenue"]

        # 按日期
        d = by_date.setdefault(r["date"], {"qty": 0, "revenue": 0.0})
        d["qty"]     += r["qty"]
        d["revenue"] += r["revenue"]

    total_revenue = sum(r["revenue"] for r in records)
    total_qty     = sum(r["qty"]     for r in records)

    # ── Step 3：找出最佳销售员和最热销产品 ──
    top_seller  = max(by_seller,  key=lambda k: by_seller[k]["revenue"])
    top_product = max(by_product, key=lambda k: by_product[k]["revenue"])

    # ── Step 4：组装结果字典 ──
    return {
        "summary": {
            "total_revenue": round(total_revenue, 2),
            "total_qty":     total_qty,
            "record_count":  len(records),
            "date_range":    f"{min(r['date'] for r in records)} ~ {max(r['date'] for r in records)}",
            "top_seller":    top_seller,
            "top_product":   top_product,
        },
        "by_seller":  {k: {kk: round(vv, 2) for kk, vv in v.items()}
                       for k, v in sorted(by_seller.items())},
        "by_product": {k: {kk: round(vv, 2) for kk, vv in v.items()}
                       for k, v in sorted(by_product.items(), key=lambda x: -x[1]["revenue"])},
        "by_date":    {k: {kk: round(vv, 2) for kk, vv in v.items()}
                       for k, v in sorted(by_date.items())},
        "generated_at": datetime.now().isoformat(timespec="seconds"),  # 报告生成时间
    }

# ── 执行分析并保存结果 ──
try:
    report = analyze_sales(sales_csv)
except DataValidationError as e:
    print(f"分析失败：{e}")
    report = None

if report:
    # 打印摘要
    s = report["summary"]
    print(f"\n销售摘要（{s['date_range']}）：")
    print(f"  总营收：¥{s['total_revenue']:,.2f}")
    print(f"  总销量：{s['total_qty']} 件")
    print(f"  最佳销售员：{s['top_seller']}")
    print(f"  最热销产品：{s['top_product']}")

    print("\n各销售员业绩：")
    for seller, stat in report["by_seller"].items():
        print(f"  {seller}：营收 ¥{stat['revenue']:,.2f}，数量 {stat['qty']}")

    print("\n各产品排名：")
    for prod, stat in report["by_product"].items():
        print(f"  {prod:4s}：营收 ¥{stat['revenue']:,.2f}，数量 {stat['qty']}")

    # 保存为 JSON 文件
    output_json = WORK_DIR / "sales_report.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存：{output_json.name}（{output_json.stat().st_size} 字节）")

    # 验证：重新读取 JSON 确认数据一致
    with open(output_json, "r", encoding="utf-8") as f:
        reloaded = json.load(f)
    assert reloaded["summary"]["total_revenue"] == report["summary"]["total_revenue"], "数据不一致！"
    print("JSON 读回验证：✓ 数据与原始统计一致")

# ── 清理临时文件 ──
print("\n── 清理 ──")
import shutil
all_items = sorted(WORK_DIR.rglob("*"))
print(f"共生成 {len(all_items)} 个文件：")
for item in all_items:
    print(f"  {item.name}")
shutil.rmtree(WORK_DIR)                       # 删除整个临时目录
print(f"已清理目录：{WORK_DIR.name}/")
