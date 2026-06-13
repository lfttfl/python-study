# Python 系统学习笔记

> 从零开始，系统掌握 Python 编程，覆盖基础语法到数据分析的完整学习路径。

## 学习目标

- 扎实掌握 Python 基础语法与核心概念
- 熟练运用常用数据结构（列表、字典、集合、元组）
- 理解函数式编程思想，掌握装饰器、闭包等高阶特性
- 具备文件读写与异常处理能力
- 系统掌握面向对象编程（类、继承、多态、抽象基类）
- 熟悉标准库常用模块（collections、pathlib、heapq 等）
- 能够使用 NumPy、Pandas 进行数据分析与处理

## 目录说明

| 目录 | 主题 | 内容概览 |
|------|------|----------|
| [01_basics](./01_basics/) | 基础语法 | 变量、数据类型、条件判断、循环、函数、推导式 |
| [02_data_structures](./02_data_structures/) | 数据结构 | 列表、元组、字典、集合及其常用操作 |
| [03_functions](./03_functions/) | 函数进阶 | 闭包、装饰器、递归、高阶函数、迭代器、生成器 |
| [04_file_io](./04_file_io/) | 文件读写 | 文件操作、CSV/JSON 读写、异常处理 |
| [05_data_analysis](./05_data_analysis/) | 数据分析 | NumPy 数组、Pandas DataFrame、数据清洗与可视化 |
| [06_oop](./06_oop/) | 面向对象 | 类与实例、魔法方法、继承、多态、抽象基类、dataclass |
| [07_stdlib](./07_stdlib/) | 标准库 | collections、heapq、bisect、pathlib、异常处理进阶 |

## 学习路线

```
01_basics → 02_data_structures → 03_functions → 04_file_io → 06_oop → 07_stdlib → 05_data_analysis
```

每个模块包含详细注释的示例代码和末尾的练习题（附参考答案）。

## 运行测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行所有测试
pytest tests/ -v

# 运行单个文件
python 01_basics/01_variables.py
```

## 环境要求

- Python 3.10+
- 依赖库：见 `requirements.txt`

```bash
pip install -r requirements.txt
```

## 模块详情

### 06_oop（面向对象编程）

| 文件 | 内容 |
|------|------|
| `01_classes_basics.py` | 类定义、实例变量、类变量、魔法方法（`__repr__`、`__eq__`、`__hash__`、`__iter__`）、`classmethod`、`staticmethod`、`__slots__` |
| `02_inheritance.py` | 单继承、`super()`、多态、抽象基类（`ABC`、`@abstractmethod`）、多重继承、Mixin 模式 |
| `03_dataclass_property.py` | `@property`（getter/setter/deleter）、`@dataclass`、`field()`、`__post_init__`、上下文管理器（`__enter__`/`__exit__`、`@contextmanager`） |

### 07_stdlib（标准库）

| 文件 | 内容 |
|------|------|
| `01_collections_advanced.py` | `Counter`（计数器）、`defaultdict`（默认字典）、`deque`（双端队列）、`ChainMap`（链式查找）、`heapq`（堆/优先队列）、`bisect`（二分查找） |
| `02_pathlib_exceptions.py` | `pathlib.Path`（现代文件路径操作）、异常链（`raise from`）、自定义异常层次、`traceback` 模块、异常处理最佳实践 |

## 参考资源

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [NumPy 官方文档](https://numpy.org/doc/)
- [Pandas 官方文档](https://pandas.pydata.org/docs/)
- [pytest 文档](https://docs.pytest.org/)
