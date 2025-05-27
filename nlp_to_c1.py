import tkinter as tk
from tkinter import scrolledtext
import subprocess
import tempfile

def nlp_to_c(nlp_lines):
    c_code = []
    for line in nlp_lines:
        line = line.lower().strip()

        if line.startswith("print "):
            content = line[6:]
            if not (content.startswith('"') and content.endswith('"')):
                c_code.append(f'printf("%d\\n", {content});')
            else:
                c_code.append(f'printf({content} );')

        elif line.startswith("declare int "):
            var_name = line[len("declare int "):].strip()
            c_code.append(f'int {var_name};')

        elif line.startswith("set "):
            parts = line[len("set "):].split(" to ")
            if len(parts) == 2:
                var, val = parts[0].strip(), parts[1].strip()
                c_code.append(f'{var} = {val};')

        elif line.startswith("if "):
            cond = line[3:]
            cond = cond.replace("greater than", ">")
            cond = cond.replace("less than", "<")
            cond = cond.replace("equals", "==")
            c_code.append(f'if ({cond})' + ' {')

        elif line == "else":
            c_code.append('} else {')

        elif line == "end if":
            c_code.append('}')

        elif line.startswith("loop from "):
            import re
            match = re.match(r'loop from (\w+) equals (\d+) to (\d+)', line)
            if match:
                var, start, end = match.groups()
                c_code.append(f'for (int {var} = {start}; {var} <= {end}; {var}++)' + ' {')

        elif line == "end loop":
            c_code.append('}')

        elif line.startswith("return "):
            val = line[len("return "):].strip()
            c_code.append(f'return {val};')

        else:
            c_code.append(f'// Unsupported instruction: {line}')

    indented = "\n".join("    " + stmt for stmt in c_code)
    return '#include <stdio.h>\n\nint main() {\n' + indented + '\n    return 0;\n}'

def compile_c_code(c_code):
    try:
        with tempfile.NamedTemporaryFile(suffix=".c", mode='w', delete=False) as cfile:
            cfile.write(c_code)
            cfilename = cfile.name

        exe_file = cfilename[:-2]  # remove .c

        compile_process = subprocess.run(['gcc', cfilename, '-o', exe_file], capture_output=True, text=True)
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_process.stderr}"

        run_process = subprocess.run([exe_file], capture_output=True, text=True)
        if run_process.returncode != 0:
            return f"Runtime Error:\n{run_process.stderr}"

        return run_process.stdout or "Program executed successfully with no output."
    except Exception as e:
        return f"Error: {e}"

def run_code():
    nlp_input = nlp_text.get("1.0", tk.END).strip().split('\n')
    if not nlp_input or nlp_input == ['']:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please enter some NLP instructions.")
        return

    c_code = nlp_to_c(nlp_input)

    # Clear old text before inserting new
    c_code_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

    c_code_text.insert(tk.END, c_code)

    output = compile_c_code(c_code)
    output_text.insert(tk.END, output)

root = tk.Tk()
root.title("NLP to C Compiler GUI")
root.geometry("1000x700")
root.configure(bg='lemon chiffon')

# Fonts
import tkinter.font as tkFont
my_font = tkFont.Font(family="Helvetica", size=16)

# NLP input area
tk.Label(root, text="Enter NLP Instructions (one per line):", bg='lemon chiffon', font=my_font).pack(pady=(10, 0))
nlp_text = scrolledtext.ScrolledText(root, height=10, width=80, font=my_font)
nlp_text.pack(padx=10, pady=5)
nlp_text.config(bg='lightyellow')

run_button = tk.Button(root, text="Generate & Run", bg='gold', font=my_font, command=run_code)
run_button.pack(pady=5)

# Frame to hold C code and output side-by-side
bottom_frame = tk.Frame(root, bg='lemon chiffon')
bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Left side: C code
left_frame = tk.Frame(bottom_frame, bg='lemon chiffon')
left_frame.pack(side='left', fill='both', expand=True)

tk.Label(left_frame, text="Generated C Code:", bg='lemon chiffon', font=my_font).pack()
c_code_text = scrolledtext.ScrolledText(left_frame, height=25, width=50, font=my_font)
c_code_text.pack(fill='both', expand=True)
c_code_text.config(bg='lightyellow')

# Right side: Output
right_frame = tk.Frame(bottom_frame, bg='lemon chiffon')
right_frame.pack(side='left', fill='both', expand=True, padx=(10,0))

tk.Label(right_frame, text="Program Output:", bg='lemon chiffon', font=my_font).pack()
output_text = scrolledtext.ScrolledText(right_frame, height=25, width=50, font=my_font)
output_text.pack(fill='both', expand=True)
output_text.config(bg='lightyellow')

root.mainloop()
