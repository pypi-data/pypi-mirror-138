import ast
import inspect
from .ast_tree_builder import AstTreeBuilder


def fib(n: int):
    nums = [0, 1]
    if n <= 0:
        raise RuntimeError()
    if n <= 2:
        return nums[:n]
    for i in range(2, n):
        nums.append(nums[i - 1] + nums[i - 2])
    return nums


def get_ast_picture(filename: str = 'picture', format_: str = 'png', function=fib):
    code = inspect.getsource(function)
    ast_object = ast.parse(code)
    builder = AstTreeBuilder()
    builder.build(ast_object)
    builder.G.render(format=format_, filename=filename, cleanup=True)


if __name__ == '__main__':
    get_ast_picture()
