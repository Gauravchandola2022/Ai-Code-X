# targetcode_runner.py

from lexer import lexer 
from parser import parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from executor import Executor
import io
import sys

def run_code_with_compiler(user_code: str):
    # Redirect stdout to capture prints from Executor.run()
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        # Step 1: Lexing
        lexer.input(user_code)

        # Step 2: Parsing → AST
        ast = parser.parse(user_code, lexer=lexer)

        # Step 3: Semantic Analysis
        SemanticAnalyzer().analyze(ast)

        # Step 4: IR Generation
        ir = IRGenerator()
        ir.generate(ast)

        # Step 5: Optimization
        opt = Optimizer(ir.code)
        opt.optimize()

        # Step 6: Execution
        result = Executor(opt.get_code)
        result.run()
    except Exception as e:
        print("error", e)

    # Restore stdout
    sys.stdout = old_stdout

    # Return captured output
    return mystdout.getvalue()
