"""簡単な電卓プログラム。

四則演算・剰余・べき乗・括弧に対応します。
使い方:
    python calculator.py            # 対話モード
    python calculator.py "1 + 2*3"  # 1回だけ計算
"""

import ast
import operator
import sys

BINARY_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPS:
        return BINARY_OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
        return UNARY_OPS[type(node.op)](_eval(node.operand))
    raise ValueError("使用できない式です")


def calculate(expression):
    """文字列の数式を計算して結果を返す。"""
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("式の形式が正しくありません") from None
    try:
        return _eval(tree)
    except ZeroDivisionError:
        raise ValueError("0で割ることはできません") from None


def main():
    if len(sys.argv) > 1:
        try:
            print(calculate(" ".join(sys.argv[1:])))
        except ValueError as e:
            print(f"エラー: {e}")
            sys.exit(1)
        return

    print("電卓 (終了: q / quit)")
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.lower() in ("q", "quit", "exit"):
            break
        if not line:
            continue
        try:
            print(calculate(line))
        except ValueError as e:
            print(f"エラー: {e}")


if __name__ == "__main__":
    main()
