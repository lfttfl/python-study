# Python 标准库：pathlib 现代文件路径 + 异常处理进阶
# =====================================================

from pathlib import Path
import os, sys, traceback

# ══════════════════════════════════════════════════════
# 一、pathlib：现代文件路径操作
# ══════════════════════════════════════════════════════

print("══ 一、pathlib.Path ══")

# pathlib 提供面向对象的路径操作，比 os.path 更直观，跨平台更友好
# Path 对象自动处理不同操作系统的路径分隔符（/ 或 \）

# ── 创建 Path 对象 ──
cwd   = Path.cwd()                             # 当前工作目录
home  = Path.home()                            # 用户主目录
p     = Path("/home/user/python-study")        # 绝对路径
rel   = Path("data/input.csv")                 # 相对路径

print(f"当前目录：{cwd}")
print(f"主目录：  {home}")
print(f"Path 类型：{type(p)}")

# ── 路径拼接：/ 运算符 ──
print("\n── 路径拼接 ──")

base    = Path("/home/user/project")
src     = base / "src"                         # 比 os.path.join 更直观
config  = base / "config" / "settings.yaml"
print(f"src：    {src}")
print(f"config： {config}")

# ── 路径属性 ──
print("\n── 路径属性 ──")

p = Path("/home/user/project/src/main.py")
print(f"name：     {p.name}")                  # main.py（文件名+扩展名）
print(f"stem：     {p.stem}")                  # main（文件名无扩展名）
print(f"suffix：   {p.suffix}")                # .py（扩展名）
print(f"suffixes： {Path('archive.tar.gz').suffixes}")  # ['.tar', '.gz']
print(f"parent：   {p.parent}")                # /home/user/project/src
print(f"parents：  {list(p.parents)}")         # 所有上级路径
print(f"parts：    {p.parts}")                 # ('/', 'home', 'user', ...)
print(f"root：     {p.root}")                  # /
print(f"is_absolute：{p.is_absolute()}")        # True

# ── 路径变换 ──
print("\n── 路径变换 ──")

p = Path("data/input.csv")
print(f"with_name：{p.with_name('output.csv')}")      # data/output.csv
print(f"with_stem：{p.with_stem('result')}")           # data/result.csv
print(f"with_suffix：{p.with_suffix('.json')}")        # data/input.json

# ── 文件系统操作 ──
print("\n── 文件系统操作 ──")

# 用临时目录演示，避免污染真实目录
import tempfile, shutil

tmp_dir = Path(tempfile.mkdtemp())
print(f"临时目录：{tmp_dir}")

# 创建目录
(tmp_dir / "subdir" / "nested").mkdir(parents=True, exist_ok=True)
(tmp_dir / "empty").mkdir(exist_ok=True)

# 创建文件
(tmp_dir / "hello.txt").write_text("Hello, pathlib!\n第二行", encoding="utf-8")
(tmp_dir / "data.csv").write_text("name,score\n小明,88\n小红,92", encoding="utf-8")
(tmp_dir / "subdir" / "nested" / "deep.txt").write_text("深层文件", encoding="utf-8")

# 读文件
content = (tmp_dir / "hello.txt").read_text(encoding="utf-8")
print(f"读取文件：{repr(content)}")

data_bytes = (tmp_dir / "hello.txt").read_bytes()
print(f"读取字节：{data_bytes[:10]}")

# 文件状态检查
txt_path = tmp_dir / "hello.txt"
print(f"\nexists：  {txt_path.exists()}")
print(f"is_file： {txt_path.is_file()}")
print(f"is_dir：  {tmp_dir.is_dir()}")

stat = txt_path.stat()
print(f"文件大小：{stat.st_size} 字节")

# 遍历目录
print("\n── 遍历目录 ──")
print("iterdir（一层）：")
for item in sorted(tmp_dir.iterdir()):
    print(f"  {'📁' if item.is_dir() else '📄'} {item.name}")

# glob：匹配模式查找文件（支持 *、**、?）
print("\nglob('**/*.txt')：所有 .txt 文件：")
for f in sorted(tmp_dir.glob("**/*.txt")):    # ** 递归匹配所有子目录
    print(f"  {f.relative_to(tmp_dir)}")       # relative_to 转为相对路径

print("\nrglob('*.txt')：等价写法：")
for f in sorted(tmp_dir.rglob("*.txt")):      # rglob 是 glob('**/*.txt') 的简写
    print(f"  {f.relative_to(tmp_dir)}")

# 文件操作
print("\n── 文件操作 ──")
src  = tmp_dir / "hello.txt"
dst  = tmp_dir / "hello_copy.txt"
src.rename(tmp_dir / "hello_renamed.txt")      # 重命名（原文件消失）
(tmp_dir / "hello_renamed.txt").replace(dst)   # replace：覆盖目标（如果存在）

new_file = tmp_dir / "new.txt"
new_file.touch()                               # 创建空文件（或更新时间戳）
new_file.unlink()                              # 删除文件
new_file.unlink(missing_ok=True)               # missing_ok=True：文件不存在也不报错

# 清理
shutil.rmtree(tmp_dir)
print(f"清理后存在：{tmp_dir.exists()}")        # False

# ── Path 与字符串的互换 ──
print("\n── Path 与字符串 ──")

p = Path("/home/user/data.csv")
print(f"str(p)：{str(p)}")                     # 转为字符串
print(f"os.fspath(p)：{os.fspath(p)}")         # 效果相同，更通用
# 大多数接受字符串路径的函数也接受 Path 对象（Python 3.6+）

# ══════════════════════════════════════════════════════
# 二、异常处理进阶
# ══════════════════════════════════════════════════════

print("\n══ 二、异常处理进阶 ══")

# ── 异常继承体系 ──
print("\n── 异常继承体系 ──")

# BaseException（根基类）
# ├── SystemExit          # sys.exit() 触发
# ├── KeyboardInterrupt   # Ctrl+C 触发
# ├── GeneratorExit       # 生成器关闭时触发
# └── Exception           # 普通异常的根基类
#     ├── ValueError
#     ├── TypeError
#     ├── KeyError
#     ├── IndexError
#     ├── FileNotFoundError（← OSError ← IOError）
#     ├── RuntimeError
#     └── ...

# ── try/except/else/finally 完整语法 ──
print("\n── 完整异常处理语法 ──")

def divide_file_content(path, divisor):
    """演示完整的异常处理流程"""
    try:
        # try 块：可能引发异常的代码
        with open(path) as f:
            value = int(f.read().strip())
        result = value / divisor

    except FileNotFoundError as e:
        # 处理特定异常（越具体的异常放越前面）
        print(f"  文件不存在：{e}")
        return None

    except (ValueError, TypeError) as e:
        # 一个 except 可以处理多种异常
        print(f"  数据格式错误：{e}")
        return None

    except ZeroDivisionError:
        print("  除数不能为 0")
        return None

    except Exception as e:
        # 兜底：捕获所有未明确处理的异常（应尽量具体，避免吞掉意外错误）
        print(f"  未预期的错误：{type(e).__name__}: {e}")
        return None

    else:
        # else 块：try 块没有异常时才执行（用于把"成功路径"的代码与异常处理分开）
        print(f"  计算成功：{result}")
        return result

    finally:
        # finally 块：无论是否有异常都执行（清理资源的最后防线）
        print("  [finally] 执行清理")

divide_file_content("/不存在的文件.txt", 2)
print()

# ── 异常链：raise from ──
print("\n── 异常链（raise from）──")

def load_config(path):
    try:
        data = Path(path).read_text()
        import json
        return json.loads(data)
    except FileNotFoundError as e:
        # raise X from Y：显式声明 X 是由 Y 引起的，保留原始异常信息
        raise RuntimeError(f"配置文件缺失：{path}") from e
    except Exception as e:
        raise RuntimeError(f"配置文件无效：{path}") from e

try:
    load_config("/etc/myapp/config.json")
except RuntimeError as e:
    print(f"上层异常：{e}")
    print(f"原始异常：{e.__cause__}")          # __cause__ 是链接的原始异常
    print(f"异常链：{type(e).__name__} → {type(e.__cause__).__name__}")

# raise from None：隐藏原始异常（适合用户不需要看到内部细节时）
def get_user(user_id):
    try:
        db = {}                                # 模拟数据库
        return db[user_id]
    except KeyError:
        raise ValueError(f"用户 {user_id} 不存在") from None  # 隐藏 KeyError

try:
    get_user(999)
except ValueError as e:
    print(f"用户查询：{e}（原始异常已隐藏）")

# ── 自定义异常 ──
print("\n── 自定义异常 ──")

# 自定义异常：继承 Exception（或更具体的子类），按业务域分层组织

class AppError(Exception):
    """应用级基础异常：所有自定义异常的根"""
    pass

class ValidationError(AppError):
    """数据验证失败"""
    def __init__(self, field, value, reason):
        self.field  = field
        self.value  = value
        self.reason = reason
        super().__init__(f"字段 '{field}'='{value}' 验证失败：{reason}")

class AuthenticationError(AppError):
    """认证失败"""
    def __init__(self, username):
        self.username = username
        super().__init__(f"用户 '{username}' 认证失败")

class PermissionError_(AppError):             # 加 _ 避免覆盖内置 PermissionError
    """权限不足"""
    def __init__(self, user, action, resource):
        super().__init__(f"用户 '{user}' 无权执行 '{action}' 于 '{resource}'")


def process_age(value):
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValidationError("age", value, "必须是整数") from None
    if not (0 <= age <= 150):
        raise ValidationError("age", age, "必须在 0-150 之间")
    return age


for test_val in ["abc", -5, 25, 200]:
    try:
        result = process_age(test_val)
        print(f"  age={test_val} → 合法：{result}")
    except ValidationError as e:
        print(f"  age={test_val} → {e}")

# 捕获整个异常层次
print("\n── 按异常层次捕获 ──")
errors = [
    ValidationError("email", "bad", "格式不对"),
    AuthenticationError("hacker"),
]
for err in errors:
    if isinstance(err, AppError):
        print(f"  应用异常：{err}")

# ── traceback 模块：手动处理异常信息 ──
print("\n── traceback 模块 ──")

def risky():
    return 1 / 0

try:
    risky()
except ZeroDivisionError:
    # traceback.format_exc()：把当前异常的完整堆栈转为字符串（常用于日志记录）
    tb_str = traceback.format_exc()
    print(f"异常信息（前两行）：")
    for line in tb_str.strip().split("\n")[:3]:
        print(f"  {line}")

# ── ExceptionGroup（Python 3.11+）：同时处理多个异常 ──
print("\n── 最佳实践小结 ──")
print("""
异常处理最佳实践：
  1. 捕获具体异常，不要裸用 except:（会吞掉 KeyboardInterrupt 等）
  2. 只捕获能处理的异常，其他的让它向上传播
  3. 在模块边界处用自定义异常封装内部细节（raise from）
  4. finally 用于清理资源（比 close()/del 更可靠）
  5. else 块用于成功路径，和异常处理路径分开，提高可读性
  6. 不要用异常控制正常流程（有专门的 if/else 逻辑）
""")

# ══════════════════════════════════════════════════════
# 练习题
# ══════════════════════════════════════════════════════

print("══ 练习题 ══")
print("""
1. 用 pathlib 实现函数 find_duplicates(directory)：
   扫描给定目录下所有文件，返回 {文件名: [重复文件路径列表]} 的字典
   （同名文件在不同子目录下算重复）。

2. 定义异常层次：
   NetworkError（基类）→ TimeoutError、ConnectionRefused、DNSError
   实现函数 fetch(url, timeout)，根据情况抛出对应的具体异常，
   调用方只需 except NetworkError 即可统一处理。

3. 实现上下文管理器 safe_write(path)（用 contextmanager 装饰器）：
   进入时创建临时文件，成功退出时原子替换目标文件，
   异常退出时删除临时文件并重新抛出异常。

参考答案见下方注释：
""")

# # 答案2：
# class NetworkError(Exception): pass
# class TimeoutError_(NetworkError):
#     def __init__(self, url, timeout): super().__init__(f"请求 {url} 超时（>{timeout}s）")
# class ConnectionRefused(NetworkError):
#     def __init__(self, url): super().__init__(f"连接被拒绝：{url}")
# class DNSError(NetworkError):
#     def __init__(self, host): super().__init__(f"DNS 解析失败：{host}")
#
# def fetch(url, timeout=5):
#     import random
#     choice = random.choice(["ok", "timeout", "refused", "dns"])
#     if choice == "timeout":   raise TimeoutError_(url, timeout)
#     if choice == "refused":   raise ConnectionRefused(url)
#     if choice == "dns":       raise DNSError(url.split("/")[2] if "/" in url else url)
#     return f"<html>内容来自 {url}</html>"
#
# for _ in range(5):
#     try:
#         print(fetch("http://example.com"))
#     except NetworkError as e:
#         print(f"网络错误：{e}")
