"""
测试项目中的纯函数。
运行方式：在项目根目录执行 pytest tests/ -v
"""

import pytest
import sys
from pathlib import Path

# 把项目根目录加入模块搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# ══════════════════════════════════════════════════════
# 从各模块导入被测函数
# ══════════════════════════════════════════════════════

# 为了直接 import，需要把各模块内的函数提取出来单独测试
# 这里用内联重新定义，方便运行（无需执行各模块的 print 语句）

# ── 来自 03_functions/01_advanced_functions.py ──

def factorial_recursive(n):
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    if n < 0:
        raise ValueError("n 必须是非负整数")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fib_iterative(n):
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def fib_memo(n, memo=None):
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


def flatten_recursive(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_recursive(item))
        else:
            result.append(item)
    return result


# ── 来自 01_basics/01_variables.py 的类型转换逻辑 ──

def safe_int(value):
    """安全地把字符串或浮点数转为整数，失败返回 None"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


# ── 来自 03_functions/01_advanced_functions.py 的管道工具 ──

def compose(*funcs):
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed


def pipe(*funcs):
    def piped(x):
        result = x
        for func in funcs:
            result = func(result)
        return result
    return piped


# ══════════════════════════════════════════════════════
# 阶乘测试
# ══════════════════════════════════════════════════════

class TestFactorial:
    def test_zero(self):
        assert factorial_recursive(0) == 1
        assert factorial_iterative(0) == 1

    def test_one(self):
        assert factorial_recursive(1) == 1
        assert factorial_iterative(1) == 1

    def test_small_values(self):
        expected = {2: 2, 3: 6, 4: 24, 5: 120, 6: 720}
        for n, expected_val in expected.items():
            assert factorial_recursive(n) == expected_val, f"factorial({n}) 应为 {expected_val}"
            assert factorial_iterative(n) == expected_val

    def test_large_value(self):
        assert factorial_recursive(10) == 3628800
        assert factorial_iterative(10) == 3628800

    def test_recursive_equals_iterative(self):
        for n in range(15):
            assert factorial_recursive(n) == factorial_iterative(n), \
                f"recursive({n}) != iterative({n})"

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="非负整数"):
            factorial_recursive(-1)
        with pytest.raises(ValueError, match="非负整数"):
            factorial_iterative(-1)


# ══════════════════════════════════════════════════════
# 斐波那契数列测试
# ══════════════════════════════════════════════════════

class TestFibonacci:
    KNOWN = {0: 0, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 8: 21, 9: 34, 10: 55}

    def test_base_cases(self):
        assert fib_iterative(0) == 0
        assert fib_iterative(1) == 1
        assert fib_memo(0) == 0
        assert fib_memo(1) == 1

    def test_known_values(self):
        for n, expected in self.KNOWN.items():
            assert fib_iterative(n) == expected, f"fib_iterative({n}) 应为 {expected}"
            assert fib_memo(n) == expected, f"fib_memo({n}) 应为 {expected}"

    def test_iterative_equals_memo(self):
        for n in range(20):
            assert fib_iterative(n) == fib_memo(n)

    def test_memo_no_shared_state(self):
        # 验证修复后的 fib_memo 不会因为 memo={} 可变默认参数产生跨调用污染
        result1 = fib_memo(10)
        result2 = fib_memo(10)              # 第二次调用应使用新的 memo，结果相同
        assert result1 == result2 == 55

    def test_large_value(self):
        assert fib_iterative(30) == 832040
        assert fib_memo(30) == 832040


# ══════════════════════════════════════════════════════
# 嵌套列表展开测试
# ══════════════════════════════════════════════════════

class TestFlatten:
    def test_empty(self):
        assert flatten_recursive([]) == []

    def test_flat_list(self):
        assert flatten_recursive([1, 2, 3]) == [1, 2, 3]

    def test_one_level_nested(self):
        assert flatten_recursive([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_deeply_nested(self):
        assert flatten_recursive([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]

    def test_mixed_depth(self):
        assert flatten_recursive([1, [2, 3], [4, [5, 6]], [[7], 8]]) == [1, 2, 3, 4, 5, 6, 7, 8]

    def test_preserves_order(self):
        result = flatten_recursive([[3, 1], [2], [4, 5]])
        assert result == [3, 1, 2, 4, 5]

    def test_mixed_types(self):
        result = flatten_recursive([1, ["a", [True, None]]])
        assert result == [1, "a", True, None]

    def test_original_not_modified(self):
        original = [[1, 2], [3, [4]]]
        flatten_recursive(original)
        assert original == [[1, 2], [3, [4]]]  # 原列表不应被修改


# ══════════════════════════════════════════════════════
# safe_int 测试
# ══════════════════════════════════════════════════════

class TestSafeInt:
    def test_valid_string(self):
        assert safe_int("42") == 42
        assert safe_int("-10") == -10
        assert safe_int("0") == 0

    def test_float_truncation(self):
        assert safe_int(3.99) == 3
        assert safe_int(3.01) == 3

    def test_invalid_string_returns_none(self):
        assert safe_int("abc") is None
        assert safe_int("1.5") is None   # int("1.5") 会失败
        assert safe_int("") is None

    def test_none_returns_none(self):
        assert safe_int(None) is None


# ══════════════════════════════════════════════════════
# compose 和 pipe 测试
# ══════════════════════════════════════════════════════

class TestComposePipe:
    def test_compose_two_functions(self):
        double = lambda x: x * 2
        inc    = lambda x: x + 1
        # compose(f, g)(x) = f(g(x))，先 g 后 f
        f = compose(double, inc)
        assert f(3) == 8   # inc(3)=4, double(4)=8

    def test_pipe_two_functions(self):
        double = lambda x: x * 2
        inc    = lambda x: x + 1
        # pipe(f, g)(x) = g(f(x))，先 f 后 g
        f = pipe(double, inc)
        assert f(3) == 7   # double(3)=6, inc(6)=7

    def test_compose_identity(self):
        identity = lambda x: x
        f = compose(identity)
        assert f(42) == 42

    def test_pipe_string_operations(self):
        process = pipe(str.strip, str.upper, lambda s: s + "!")
        assert process("  hello  ") == "HELLO!"

    def test_compose_is_reverse_of_pipe(self):
        funcs = [lambda x: x + 1, lambda x: x * 2, lambda x: x - 3]
        composed_result = compose(*funcs)(10)
        piped_result    = pipe(*reversed(funcs))(10)
        assert composed_result == piped_result

    def test_three_functions(self):
        f = pipe(lambda x: x + 1, lambda x: x * 2, lambda x: x ** 2)
        assert f(3) == ((3 + 1) * 2) ** 2   # 4 * 2 = 8, 8^2 = 64


# ══════════════════════════════════════════════════════
# 参数化测试示例
# ══════════════════════════════════════════════════════

@pytest.mark.parametrize("n,expected", [
    (0, 1),
    (1, 1),
    (5, 120),
    (10, 3628800),
    (12, 479001600),
])
def test_factorial_parametrized(n, expected):
    assert factorial_iterative(n) == expected
    assert factorial_recursive(n) == expected


@pytest.mark.parametrize("input_list,expected", [
    ([], []),
    ([1, 2, 3], [1, 2, 3]),
    ([[1], [2], [3]], [1, 2, 3]),
    ([1, [2, [3]]], [1, 2, 3]),
])
def test_flatten_parametrized(input_list, expected):
    assert flatten_recursive(input_list) == expected
