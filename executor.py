class Executor:
    def __init__(self, ir_lines):
        self.env = {}
        self.lines = ir_lines

    def eval_expr(self, expr):
        tokens = expr.split()
        if len(tokens) == 1:
            # Could be variable or no.
            val = self.env.get(tokens[0])
            if val is not None:
                return val
            else:
                return int(tokens[0])
        elif len(tokens) == 3:
            left = self.env.get(tokens[0], tokens[0])
            right = self.env.get(tokens[2], tokens[2])
            left = int(left) if isinstance(left, str) and left.isdigit() else left
            right = int(right) if isinstance(right, str) and right.isdigit() else right

            if isinstance(left, str):
                left = int(left)
            if isinstance(right, str):
                right = int(right)

            op = tokens[1]
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left // right

    def run(self):
        for line in self.lines:
            if line.startswith("return"):
                expr = line[len("return"):].strip()
                result = self.eval_expr(expr)
                print(f"\nProgram Returned: {result}")
                return result

            var, expr = line.split("=", 1)
            var = var.strip()
            expr = expr.strip()
            self.env[var]= self.eval_expr(expr)
