# Python 文件 I/O 练习：文件读写、路径处理、编码
# =====================================================

import os                                     # 操作系统接口：文件/目录操作、环境变量等
import os.path                                # 路径操作的传统方式（字符串风格）
from pathlib import Path                      # 路径操作的现代方式（面向对象风格，推荐）
import shutil                                 # 高级文件操作：复制、移动、删除目录树
import tempfile                               # 创建临时文件/目录，程序退出后自动清理

# 把所有练习产生的文件统一放到 tmp_practice/ 目录，方便清理
WORK_DIR = Path(__file__).parent / "tmp_practice"   # __file__ 是当前脚本的绝对路径
WORK_DIR.mkdir(exist_ok=True)                 # exist_ok=True：目录已存在时不报错

print(f"工作目录：{WORK_DIR}")

# ══════════════════════════════════════════════════════
# 一、文件写入
# ══════════════════════════════════════════════════════

print("\n══ 一、文件写入 ══")

# ── 1-1 open() 的模式参数 ─────────────────────────────

# open(file, mode, encoding) 是打开文件的内置函数
# mode 常用值：
#   'r'  只读（默认），文件不存在则报 FileNotFoundError
#   'w'  只写，文件不存在则创建，已存在则清空重写
#   'a'  追加写，文件不存在则创建，已存在则在末尾追加
#   'x'  独占创建，文件已存在则报 FileExistsError（防覆盖）
#   'b'  二进制模式（与上面的字母组合：'rb'、'wb'）
#   '+'  读写模式（与上面组合：'r+'、'w+'）
# encoding：文本模式必须指定，推荐统一用 'utf-8'

# ── 1-2 手动管理文件（了解原理，生产代码用 with）────────

sample_path = WORK_DIR / "sample.txt"         # 用 / 拼接路径（pathlib 重载了除法运算符）

f = open(sample_path, "w", encoding="utf-8")  # 打开文件：'w' 写模式，指定 UTF-8 编码
f.write("第一行：Python 文件操作\n")          # write() 写入字符串，\n 是换行符，返回写入字符数
f.write("第二行：学习 open() 函数\n")
f.write("第三行：掌握文件读写\n")
f.close()                                     # 必须手动关闭！否则缓冲区数据可能未写入磁盘
print(f"写入完成：{sample_path}")

# 手动关闭的缺点：如果 write 抛出异常，f.close() 不会被执行 → 文件泄漏

# ── 1-3 with 语句（上下文管理器，推荐写法）──────────────

print("\n── with 语句 ──")

# with open(...) as f：进入块时自动打开，退出块时自动关闭（即使发生异常也保证关闭）
# 等价于 try...finally: f.close()，但更简洁
with_path = WORK_DIR / "with_demo.txt"
with open(with_path, "w", encoding="utf-8") as f:   # f 是文件对象，块结束自动 close()
    f.write("with 语句自动管理文件生命周期\n")
    f.write("即使中途出现异常，文件也会被正确关闭\n")
    f.write("这是推荐的文件操作写法\n")
# 离开 with 块后，f 已经被关闭，再调用 f.write() 会报 ValueError
print(f"with 写入完成，文件已自动关闭：{with_path}")

# 同时打开多个文件（逗号分隔，一个 with 管理多个）
src_path = WORK_DIR / "source.txt"
dst_path = WORK_DIR / "dest.txt"
# 逗号分隔两个 open()，一个 with 同时管理两个文件对象
with (open(src_path, "w", encoding="utf-8") as src,
      open(dst_path, "w", encoding="utf-8") as dst):
    src.write("源文件内容\n")
    dst.write("目标文件内容\n")
print("同时写入两个文件完成")

# ── 1-4 writelines()：批量写入字符串列表 ────────────────

lines_path = WORK_DIR / "lines.txt"
lines = [                                     # 每行末尾必须自己加 \n，writelines 不自动换行
    "姓名,年龄,城市\n",
    "小明,18,北京\n",
    "小红,17,上海\n",
    "小刚,19,广州\n",
]
with open(lines_path, "w", encoding="utf-8") as f:
    f.writelines(lines)                       # 一次性写入列表，比循环 write() 略快
print(f"writelines 写入 {len(lines)} 行")

# ── 1-5 追加模式 'a' ──────────────────────────────────

append_path = WORK_DIR / "log.txt"
for i in range(3):                            # 模拟多次写入（比如程序多次运行）
    with open(append_path, "a", encoding="utf-8") as f:   # 'a' 模式：不清空，追加到末尾
        f.write(f"第{i+1}次写入\n")
print(f"追加模式写入完成，共追加 3 次")

# ── 1-6 print() 重定向到文件 ─────────────────────────

print_path = WORK_DIR / "print_output.txt"
with open(print_path, "w", encoding="utf-8") as f:
    print("通过 print 写入文件", file=f)       # print 的 file 参数重定向输出目标
    print("第二行", 123, [1, 2, 3], file=f)    # print 的多参数、sep、end 等特性照常可用
    print("分隔符测试", 1, 2, 3, sep="|", file=f)
print(f"print 重定向写入完成：{print_path}")

# ══════════════════════════════════════════════════════
# 二、文件读取
# ══════════════════════════════════════════════════════

print("\n══ 二、文件读取 ══")

# ── 2-1 read()：一次性读取全部内容 ───────────────────

with open(sample_path, "r", encoding="utf-8") as f:   # 'r' 是默认模式，可省略
    content = f.read()                        # 读取整个文件为一个字符串（小文件用）
print("read() 全部内容：")
print(content)                                # 包含所有换行符

# read(size)：读取指定字节数（流式读取大文件时使用）
with open(sample_path, "r", encoding="utf-8") as f:
    chunk = f.read(10)                        # 读取前 10 个字符
    print(f"read(10)：'{chunk}'")             # 前 10 个字符

# ── 2-2 readline()：每次读取一行 ──────────────────────

print("\n── readline() ──")
with open(sample_path, "r", encoding="utf-8") as f:
    line1 = f.readline()                      # 读一行（含末尾的 \n）
    line2 = f.readline()                      # 继续读下一行（文件指针向前移动）
    line3 = f.readline()
    eof   = f.readline()                      # 已到文件末尾，返回空字符串 ""（不是 None）
    print(f"第1行：{repr(line1)}")             # repr() 显示原始字符串，含 \n
    print(f"第2行：{repr(line2)}")
    print(f"第3行：{repr(line3)}")
    print(f"EOF：{repr(eof)}")                # '' 空字符串表示文件结束

# ── 2-3 readlines()：读取所有行为列表 ─────────────────

print("\n── readlines() ──")
with open(sample_path, "r", encoding="utf-8") as f:
    all_lines = f.readlines()                 # 返回字符串列表，每项含 \n
print(f"readlines() 返回 {len(all_lines)} 行：{all_lines}")

# 去掉每行末尾的 \n（常用）
clean_lines = [line.rstrip("\n") for line in all_lines]   # rstrip 只去右端换行
print("去掉换行：", clean_lines)

# ── 2-4 for 循环逐行读取（推荐：内存友好）────────────

print("\n── for 循环逐行读取 ──")
with open(lines_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):              # 文件对象本身就是迭代器，逐行惰性读取
        print(f"  [{i}] {line.rstrip()}")     # rstrip() 去掉行尾空白（含 \n \r）
# 这是处理大文件的推荐方式：任何时刻内存中只有一行

# ── 2-5 seek() 和 tell()：移动文件指针 ───────────────

print("\n── seek / tell ──")
with open(sample_path, "r", encoding="utf-8") as f:
    print("初始位置：", f.tell())             # 0：文件开头
    f.read(5)                                 # 读5个字符，指针前移
    pos = f.tell()
    print(f"读5字符后位置：{pos}")
    f.seek(0)                                 # seek(0)：回到文件开头（0 = 开头）
    print("seek(0) 后位置：", f.tell())       # 0
    first_line = f.readline()
    print(f"重新读第一行：{repr(first_line)}")

# ── 2-6 读取 CSV（不用 csv 模块，手动解析）────────────

print("\n── 手动读取 CSV ──")
with open(lines_path, "r", encoding="utf-8") as f:
    header = f.readline().rstrip().split(",") # 第一行是表头
    rows = []
    for line in f:                            # 从第二行开始是数据
        values = line.rstrip().split(",")
        row = dict(zip(header, values))       # zip 配对后转字典
        rows.append(row)

for row in rows:
    print(f"  {row}")

# ══════════════════════════════════════════════════════
# 三、文件路径处理
# ══════════════════════════════════════════════════════

print("\n══ 三、路径处理 ══")

# ── 3-1 os.path（传统方式，字符串操作）───────────────

print("── os.path ──")

script_path = os.path.abspath(__file__)       # 获取当前文件的绝对路径
print(f"当前文件绝对路径：{script_path}")

dir_name  = os.path.dirname(script_path)      # 取目录部分（去掉文件名）
base_name = os.path.basename(script_path)     # 取文件名部分（去掉目录）
print(f"目录：{dir_name}")
print(f"文件名：{base_name}")

# splitext()：分离文件名和扩展名
name, ext = os.path.splitext(base_name)       # 返回 ('01_file_operations', '.py')
print(f"主名：{name}，扩展名：{ext}")

# os.path.join()：拼接路径（自动处理不同操作系统的分隔符 / 或 \）
joined = os.path.join(dir_name, "subdir", "file.txt")
print(f"join 拼接：{joined}")

# 路径存在性检查
print(f"目录存在：{os.path.exists(dir_name)}")           # True
print(f"是目录：{os.path.isdir(dir_name)}")               # True
print(f"是文件：{os.path.isfile(script_path)}")           # True
print(f"假路径存在：{os.path.exists('/fake/path')}")       # False

# os.path.getsize()：获取文件大小（字节）
print(f"sample.txt 大小：{os.path.getsize(sample_path)} 字节")

# ── 3-2 pathlib.Path（现代方式，推荐）───────────────

print("\n── pathlib.Path ──")

p = Path(__file__)                            # 从字符串创建 Path 对象
print(f"Path 对象：{p}")
print(f"绝对路径：{p.resolve()}")             # resolve()：解析符号链接，得到绝对路径
print(f"父目录：{p.parent}")                  # parent：直接父目录
print(f"祖父目录：{p.parent.parent}")          # 链式 parent 访问
print(f"文件名：{p.name}")                    # name：含扩展名的文件名
print(f"主名（无扩展）：{p.stem}")             # stem：不含扩展名的文件名
print(f"扩展名：{p.suffix}")                  # suffix：含点的扩展名 '.py'
print(f"所有扩展名：{p.suffixes}")             # suffixes：多扩展名情况 ['.tar', '.gz']

# / 运算符拼接路径（比 os.path.join 更直观）
new_path = p.parent / "subdir" / "newfile.txt"
print(f"/ 拼接路径：{new_path}")

# 路径属性检查（与 os.path 对应）
print(f"存在：{p.exists()}")
print(f"是文件：{p.is_file()}")
print(f"是目录：{p.is_dir()}")
print(f"文件大小：{p.stat().st_size} 字节")   # stat() 返回文件元信息对象

# glob()：用通配符搜索文件（返回生成器）
print(f"\n04_file_io 目录下所有 .txt 文件：")
for txt_file in WORK_DIR.glob("*.txt"):       # * 匹配任意字符
    print(f"  {txt_file.name}")

print(f"\n03_functions 目录下所有 .py 文件（递归）：")
func_dir = p.parent.parent / "03_functions"
if func_dir.exists():
    for py_file in func_dir.rglob("*.py"):    # rglob：递归搜索所有子目录
        print(f"  {py_file.name}")

# iterdir()：遍历目录内容
print(f"\ntmp_practice 目录内容：")
for item in sorted(WORK_DIR.iterdir()):       # iterdir() 返回迭代器，sorted() 排序
    kind = "📁" if item.is_dir() else "📄"
    size = item.stat().st_size
    print(f"  {kind} {item.name:30s} {size:>6} 字节")

# Path 的文件操作方法（简化版，适合小文件）
quick_path = WORK_DIR / "quick.txt"
quick_path.write_text("一行搞定写入！\n", encoding="utf-8")   # write_text：写入并关闭
content_q = quick_path.read_text(encoding="utf-8")            # read_text：读取并关闭
print(f"\nquick_path.read_text()：{repr(content_q)}")

# ── 3-3 目录操作 ──────────────────────────────────────

print("\n── 目录操作 ──")

sub_dir = WORK_DIR / "subdir"
sub_dir.mkdir(exist_ok=True)                  # mkdir()：创建目录，exist_ok 防止重复创建
(sub_dir / "a.txt").write_text("子目录文件 A", encoding="utf-8")
(sub_dir / "b.txt").write_text("子目录文件 B", encoding="utf-8")
print(f"创建子目录：{sub_dir}")

# os.makedirs：递归创建多级目录
deep_dir = WORK_DIR / "level1" / "level2" / "level3"
os.makedirs(deep_dir, exist_ok=True)          # 一次性创建所有中间目录
print(f"递归创建多级目录：{deep_dir}")

# 重命名 / 移动文件
old_file = WORK_DIR / "quick.txt"
new_file = WORK_DIR / "renamed.txt"
old_file.rename(new_file)                     # rename()：重命名或移动（同文件系统内）
print(f"重命名：quick.txt → renamed.txt")

# shutil.copy2()：复制文件（保留元数据）
copy_dest = WORK_DIR / "copy_of_sample.txt"
shutil.copy2(sample_path, copy_dest)          # copy2：同时复制文件权限和时间戳
print(f"复制：{sample_path.name} → {copy_dest.name}")

# shutil.move()：跨文件系统也能移动
moved_file = sub_dir / "moved_sample.txt"
shutil.move(str(copy_dest), str(moved_file))  # shutil.move 接受字符串路径
print(f"移动到子目录：{moved_file.name}")

# ── 3-4 获取文件信息 ──────────────────────────────────

print("\n── 文件信息 ──")
import time as time_mod                       # 避免与之前导入的 time 混淆

stat = sample_path.stat()                     # stat() 返回 os.stat_result 对象
print(f"文件大小：{stat.st_size} 字节")
print(f"最后修改时间：{time_mod.ctime(stat.st_mtime)}")   # st_mtime 是 Unix 时间戳
print(f"最后访问时间：{time_mod.ctime(stat.st_atime)}")

# ══════════════════════════════════════════════════════
# 四、文件编码问题
# ══════════════════════════════════════════════════════

print("\n══ 四、编码处理 ══")

# ── 4-1 编码基础 ───────────────────────────────────────

# Python 字符串是 Unicode，写入文件时必须编码（Unicode → 字节）
# 读取文件时必须解码（字节 → Unicode）
# 最常见问题：写入时用 UTF-8，读取时用 GBK（或反过来）→ 乱码或报错

# UTF-8：变长编码，ASCII 字符占 1 字节，汉字占 3 字节，国际通用
# GBK（CP936）：Windows 中文版的默认编码，汉字占 2 字节，Python 中写作 'gbk' 或 'gb2312'

# ── 4-2 写入不同编码 ──────────────────────────────────

utf8_path = WORK_DIR / "utf8_file.txt"
gbk_path  = WORK_DIR / "gbk_file.txt"

with open(utf8_path, "w", encoding="utf-8") as f:
    f.write("UTF-8 编码：你好世界\n")
    f.write("中文三个字节一个汉字\n")

with open(gbk_path, "w", encoding="gbk") as f:      # 指定 GBK 编码写入
    f.write("GBK 编码：你好世界\n")
    f.write("中文两个字节一个汉字\n")

# 比较两个文件的字节大小（汉字在 UTF-8 中更大）
print(f"UTF-8 文件大小：{utf8_path.stat().st_size} 字节")
print(f"GBK  文件大小：{gbk_path.stat().st_size} 字节")

# ── 4-3 编码错误的演示与处理 ──────────────────────────

print("\n── 编码错误处理 ──")

# 用错误的编码读取文件会报 UnicodeDecodeError
try:
    with open(gbk_path, "r", encoding="utf-8") as f:  # 用 UTF-8 读 GBK 文件
        content_err = f.read()
except UnicodeDecodeError as e:
    print(f"编码错误（预期内）：{e}")

# errors 参数：控制遇到无法解码字符时的处理策略
# 'strict'（默认）：遇到错误直接抛 UnicodeDecodeError
# 'ignore'         ：跳过无法解码的字节（数据可能丢失）
# 'replace'        ：用替换字符 U+FFFD（?）代替无法解码的字节
# 'backslashreplace'：用 \xNN 转义序列表示无法解码的字节

with open(gbk_path, "r", encoding="utf-8", errors="replace") as f:
    content_replaced = f.read()              # 乱码部分变成 ?
    print(f"errors='replace' 结果：{repr(content_replaced[:30])}...")

with open(gbk_path, "r", encoding="utf-8", errors="ignore") as f:
    content_ignored = f.read()              # 乱码部分被直接忽略
    print(f"errors='ignore' 结果： {repr(content_ignored[:30])}...")

# ── 4-4 自动检测编码（chardet/charset-normalizer）──────

print("\n── 自动检测编码 ──")

# 读取文件的原始字节，手动检测编码
with open(gbk_path, "rb") as f:             # 'rb'：二进制模式读取，得到 bytes 对象
    raw_bytes = f.read()
print(f"GBK 文件原始字节（前20字节）：{raw_bytes[:20]}")

# 方法1：直接用正确编码解码
decoded_gbk = raw_bytes.decode("gbk")       # bytes.decode() 把字节解码为字符串
print(f"正确解码 GBK：{repr(decoded_gbk)}")

# 方法2：逐一尝试常见编码（简单的自动检测）
def detect_and_read(filepath):               # 尝试常见编码，返回第一个成功的结果
    encodings = ["utf-8", "utf-8-sig", "gbk", "gb2312", "latin-1"]  # 按优先级尝试
    for enc in encodings:
        try:
            return filepath.read_text(encoding=enc), enc  # 成功则返回内容和编码名
        except (UnicodeDecodeError, ValueError):
            continue                         # 失败则尝试下一种编码
    return None, None

text, enc = detect_and_read(gbk_path)
print(f"自动检测编码：{enc}，内容：{repr(text)}")

# ── 4-5 BOM（字节顺序标记）问题 ──────────────────────

print("\n── BOM 处理 ──")

# Windows 记事本保存 UTF-8 文件时会在开头加 BOM（EF BB BF），即 UTF-8-sig
bom_path = WORK_DIR / "bom_file.txt"
with open(bom_path, "w", encoding="utf-8-sig") as f:   # utf-8-sig 自动写入 BOM
    f.write("带BOM的UTF-8文件\n")
    f.write("第二行\n")

# 用 utf-8 读取会看到 BOM 字符 \ufeff
with open(bom_path, "r", encoding="utf-8") as f:
    raw = f.read()
    print(f"utf-8 读取（含BOM）：{repr(raw[:10])}")     # 开头有 \ufeff

# 用 utf-8-sig 读取会自动去掉 BOM
with open(bom_path, "r", encoding="utf-8-sig") as f:   # utf-8-sig 自动跳过 BOM
    clean = f.read()
    print(f"utf-8-sig 读取（去BOM）：{repr(clean[:10])}")

# ── 4-6 二进制文件读写 ────────────────────────────────

print("\n── 二进制读写 ──")

# 二进制模式 'rb'/'wb' 直接操作字节，不涉及编码转换
# 适用于图片、音频、压缩包等非文本文件

bin_path = WORK_DIR / "binary_demo.bin"
data = bytes(range(256))                     # bytes(range(256))：0x00 到 0xFF 共 256 字节
with open(bin_path, "wb") as f:              # 'wb'：二进制写模式
    f.write(data)

with open(bin_path, "rb") as f:              # 'rb'：二进制读模式
    read_back = f.read()
    print(f"写入 {len(data)} 字节，读回 {len(read_back)} 字节，一致：{data == read_back}")
    print(f"前8字节（十六进制）：{read_back[:8].hex(' ')}")   # hex(' ')：字节间用空格分隔

# 分块读取大型二进制文件（节省内存）
CHUNK_SIZE = 64                              # 每次读 64 字节（实际场景可用 4096、65536）
total_bytes = 0
with open(bin_path, "rb") as f:
    while True:
        chunk = f.read(CHUNK_SIZE)           # 读取一块
        if not chunk:                        # 空字节串表示文件末尾
            break
        total_bytes += len(chunk)            # 累加字节数
print(f"分块读取，共 {total_bytes} 字节")

# ══════════════════════════════════════════════════════
# 五、上下文管理器原理
# ══════════════════════════════════════════════════════

print("\n══ 五、上下文管理器原理 ══")

# with 语句依赖对象的 __enter__ 和 __exit__ 方法
# __enter__：进入 with 块时调用，返回值赋给 as 后的变量
# __exit__：退出 with 块时调用（无论是否发生异常），负责清理

class ManagedFile:                            # 手写一个上下文管理器，理解 with 的原理
    def __init__(self, path, mode, encoding="utf-8"):
        self.path     = path
        self.mode     = mode
        self.encoding = encoding
        self.file     = None

    def __enter__(self):                      # 进入 with 块：打开文件，返回文件对象
        print(f"  [ManagedFile] 打开 {Path(self.path).name}")
        self.file = open(self.path, self.mode, encoding=self.encoding)
        return self.file                      # 这个返回值就是 as 后面的变量

    def __exit__(self, exc_type, exc_val, exc_tb):   # 退出 with 块：关闭文件
        # exc_type/val/tb：异常类型、值、回溯（没有异常时都是 None）
        print(f"  [ManagedFile] 关闭文件（异常：{exc_type}）")
        if self.file:
            self.file.close()
        return False                          # 返回 False 表示不抑制异常（异常会继续传播）

custom_path = WORK_DIR / "custom_ctx.txt"
with ManagedFile(custom_path, "w") as f:     # 触发 __enter__
    f.write("自定义上下文管理器\n")
# 退出 with 块时触发 __exit__

# contextlib.contextmanager：用生成器函数快速创建上下文管理器，无需写类
from contextlib import contextmanager

@contextmanager                               # 把生成器函数变成上下文管理器
def open_file(path, mode, encoding="utf-8"):
    print(f"  [contextmanager] 打开 {Path(path).name}")
    f = open(path, mode, encoding=encoding)   # 准备资源（相当于 __enter__）
    try:
        yield f                               # yield 的值赋给 as 后的变量；yield 后暂停
    finally:                                  # finally 保证无论是否异常都会执行
        print(f"  [contextmanager] 关闭文件")
        f.close()                             # 清理资源（相当于 __exit__）

ctx_path = WORK_DIR / "ctx_manager.txt"
with open_file(ctx_path, "w") as f:
    f.write("contextmanager 装饰器创建的上下文管理器\n")

# ══════════════════════════════════════════════════════
# 六、综合示例：日志文件分析器
# ══════════════════════════════════════════════════════

print("\n══ 六、综合示例：日志分析 ══")

# 生成测试日志文件
log_file = WORK_DIR / "app.log"
log_entries = [
    "2024-04-20 10:00:01 INFO  服务器启动\n",
    "2024-04-20 10:00:02 DEBUG 配置加载：port=8080\n",
    "2024-04-20 10:01:15 INFO  用户登录：user_id=1001\n",
    "2024-04-20 10:01:33 WARN  内存使用率 75%\n",
    "2024-04-20 10:02:05 ERROR 数据库连接超时：retry=1\n",
    "2024-04-20 10:02:06 ERROR 数据库连接超时：retry=2\n",
    "2024-04-20 10:02:10 INFO  数据库重连成功\n",
    "2024-04-20 10:03:44 WARN  磁盘使用率 80%\n",
    "2024-04-20 10:04:22 ERROR 内存溢出：OOMKiller 触发\n",
    "2024-04-20 10:04:23 INFO  进程重启\n",
]
with open(log_file, "w", encoding="utf-8") as f:
    f.writelines(log_entries)

def analyze_log(path):                        # 返回各级别统计、错误详情
    stats   = {}                              # 各级别计数字典
    errors  = []                              # 错误记录列表
    total   = 0                               # 总行数

    with open(path, "r", encoding="utf-8") as f:
        for line in f:                        # 逐行读取（内存友好）
            line = line.rstrip()              # 去掉行尾空白
            if not line:                      # 跳过空行
                continue
            total += 1
            parts = line.split(" ", 3)        # 最多分割3次：日期、时间、级别、消息
            if len(parts) < 4:
                continue                      # 格式不符合预期，跳过
            date, time_str, level, msg = parts
            stats[level] = stats.get(level, 0) + 1   # 统计各级别出现次数
            if level == "ERROR":
                errors.append({"time": f"{date} {time_str}", "msg": msg})

    return total, stats, errors

total, stats, errors = analyze_log(log_file)

print(f"日志文件：{log_file.name}，共 {total} 条")
print("各级别统计：")
for level, count in sorted(stats.items()):   # 按级别名排序输出
    bar = "█" * count                        # 用方块画简单柱状图
    print(f"  {level:5s} {count:3d} {bar}")

print(f"\nERROR 详情（共 {len(errors)} 条）：")
for e in errors:
    print(f"  [{e['time']}] {e['msg']}")

# 把分析报告写入新文件
report_path = WORK_DIR / "analysis_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("=== 日志分析报告 ===\n")
    f.write(f"总条数：{total}\n\n")
    f.write("级别统计：\n")
    for level, count in sorted(stats.items()):
        f.write(f"  {level}: {count}\n")
    f.write(f"\nERROR 列表：\n")
    for e in errors:
        f.write(f"  {e['time']}  {e['msg']}\n")
print(f"\n报告已写入：{report_path.name}")

# ══════════════════════════════════════════════════════
# 七、清理临时文件（演示 shutil 删除目录树）
# ══════════════════════════════════════════════════════

print("\n══ 七、清理 ══")

# 列出工作目录所有文件（含子目录）
all_files = list(WORK_DIR.rglob("*"))         # rglob("*") 匹配所有文件和目录
print(f"共创建了 {len(all_files)} 个文件/目录：")
for item in sorted(all_files):
    rel = item.relative_to(WORK_DIR)          # relative_to：显示相对于工作目录的路径
    print(f"  {'  ' * (len(rel.parts)-1)}{rel.name}")   # 根据层级缩进

# 删除整个工作目录（含所有子目录和文件）
shutil.rmtree(WORK_DIR)                       # rmtree：递归删除，类似 rm -rf
print(f"\n已删除整个工作目录：{WORK_DIR.name}/")
print(f"目录存在：{WORK_DIR.exists()}")       # False：确认已删除
