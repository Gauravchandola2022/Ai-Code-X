from parser import parser
from lexer import lexer
from parser import Program, Function, Declaration, Return, BinOp, Number, Var

class IRGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []
        self.symbol_table = {}

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        if isinstance(node, Program):
            for fn in node.functions:
                self.generate(fn)

        elif isinstance(node, Function):
            print(f"\nFunction: {node.name}")
            for stmt in node.body:
                self.generate(stmt)

        elif isinstance(node, Declaration):
            result = self.generate(node.value)
            self.symbol_table[node.var_name] = result
            self.code.append(f"{node.var_name} = {result}")

        elif isinstance(node, Return):
            result = self.generate(node.value)
            self.code.append(f"return {result}")

        elif isinstance(node, BinOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node.op} {right}")
            return temp

        elif isinstance(node, Number):
            return str(node.value)

        elif isinstance(node, Var):
            return node.name

    def print_code(self):
        for line in self.code:
            print(line)

# ---------------- Test ---------------------

