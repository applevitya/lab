import tkinter as tk
from tkinter import ttk

def some_function(param1, param2):
    print(param1, param2)

def execute_code(code):
    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")

root = tk.Tk()
root.title("Tkinter и Matplotlib")
root.geometry("1300x800")

frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.TOP, pady=20)

# Создание первого текстового окна и кнопки для выполнения кода из него
frame_params1 = ttk.Frame(root)
frame_params1.pack(side=tk.TOP, pady=10)

text_param1 = tk.Text(root, height=10, width=50)
text_param1.insert(tk.END, "print('Hello, world!')")
text_param1.pack(side=tk.LEFT, padx=10)
btn_function1 = ttk.Button(frame_buttons, text="Выполнить код 1", command=lambda: execute_code(text_param1.get("1.0", "end-1c")))
btn_function1.pack(side=tk.LEFT, padx=10)

label_params1 = ttk.Label(frame_params1, text="Параметры функции 1:")
label_params1.pack(side=tk.TOP, pady=5)

# Создание второго текстового окна и кнопки для выполнения кода из него
text_param2 = tk.Text(root, height=10, width=50)
text_param2.insert(tk.END, "some_function('param1', 'param2')")
text_param2.pack(side=tk.LEFT, padx=10)
btn_function2 = ttk.Button(frame_buttons, text="Выполнить код 2", command=lambda: execute_code(text_param2.get("1.0", "end-1c")))
btn_function2.pack(side=tk.LEFT, padx=10)

# Создание третьего текстового окна и кнопки для выполнения кода из него
text_param3 = tk.Text(root, height=10, width=50)
text_param3.insert(tk.END, "x = 10\ny = 5\nprint(x + y)")
text_param3.pack(side=tk.LEFT, padx=10)
btn_function3 = ttk.Button(frame_buttons, text="Выполнить код 3", command=lambda: execute_code(text_param3.get("1.0", "end-1c")))
btn_function3.pack(side=tk.LEFT, padx=10)

btn_close = ttk.Button(frame_buttons, text="Закрыть", command=root.destroy)
btn_close.pack(side=tk.LEFT, padx=10)

root.mainloop()