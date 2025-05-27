import tkinter as tk
from tkinter import scrolledtext, messagebox
from nlp_to_c1 import nlp_to_c
import targetcode
import tkinter.font as tkFont
def generate_and_compile():
    nlp_text = nlp_input.get("1.0", tk.END).strip()
    if not nlp_text:
        messagebox.showwarning("Input needed", "Please enter NLP instructions.")
        return
    
    lines = nlp_text.split('\n')
    c_code = nlp_to_c(lines)

    try:
        output = targetcode.run_code_with_compiler(c_code)
    except Exception as e:
        messagebox.showerror("Compilation Error", str(e))
        return

    c_output.delete("1.0", tk.END)
    c_output.insert(tk.END, c_code)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)

root = tk.Tk()
root.title("NLP to C Compiler GUI")
root.geometry("900x700")
root.resizable(True, True)
root.configure(bg='lemon chiffon')

my_font = tkFont.Font(family="Helvetica", size=16)

tk.Label(root, text="Enter NLP Instructions (one per line):",bg='light yellow',font=my_font).pack()
nlp_input = scrolledtext.ScrolledText(root, width=60, height=15 , font=my_font)
nlp_input.pack(fill='both', expand=False, padx=10, pady=5)
nlp_input.config(bg='light yellow')



generate_btn = tk.Button(root, text="Generate and Compile", command=generate_and_compile,bg='yellow',font=my_font)
generate_btn.pack(pady=10)
#frame for layout
frame = tk.Frame(root, bg='lemon chiffon')
frame.pack(fill='both', expand=True, padx=10, pady=10)

# Left side - Generated C Code
left_frame = tk.Frame(frame, bg='lemon chiffon')
left_frame.pack(side='left', fill='both', expand=True)

tk.Label(left_frame, text="Generated C Code:",bg='light yellow',font=my_font).pack()
c_output = scrolledtext.ScrolledText(left_frame, height=20, width=40, font=my_font)
c_output.pack(fill='both', expand=True)
c_output.config(bg='light yellow')

right_frame = tk.Frame(frame, bg='lemon chiffon')
right_frame.pack(side='left', fill='both', expand=True, padx=(10,0))

tk.Label(right_frame, text="Compiler Output:",bg='light yellow',font=my_font).pack()
output_text = scrolledtext.ScrolledText(right_frame, height=20, width=40, font=my_font)
output_text.pack(fill='both', expand=True)
output_text.config(bg='light yellow')

root.mainloop()
