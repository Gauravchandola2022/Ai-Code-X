class Optimizer:
    def __init__(self, ir_lines):
        self.original = ir_lines
        self.optimized = []

    def fold_constants(self, expr):
        tokens = expr.split()
        if len(tokens) == 3:
            try:
                left = int(tokens[0])
                right = int(tokens[2])
                op = tokens[1]
                if op == '+': return str(left + right)
                if op == '-': return str(left - right)
                if op == '*': return str(left * right)
                if op == '/': return str(left // right)
            except:
                pass
        return expr

    def optimize(self):
        for line in self.original:
            if "=" in line and not line.startswith("return"):
                var, expr = line.split("=", 1)
                var = var.strip()
                expr = expr.strip()
                folded = self.fold_constants(expr)
                self.optimized.append(f"{var} = {folded}")
            else:
                self.optimized.append(line)

    def get_code(self):
        return self.optimized
