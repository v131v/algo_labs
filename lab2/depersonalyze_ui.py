import tkinter as tk
from tkinter import messagebox

from depersonalyze import *

cols = ["Passport", "Doctor", "Symptoms", "Analyzis", "DateStart", "Price", "Card"]


def run_function():
    # Получаем значение из текстового поля
    input_file = input_entry.get()

    df = pandas.read_csv(input_file)
    df = anonimyze(df)
    bad, ones, k_anon = calc_k_anonymity(
        df, list(filter(lambda name: checkboxes_vars[name].get(), cols))
    )

    # Выводим результат
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(
        tk.END,
        f"K-anonimity: {k_anon}\n"
        + "\n".join(f"Bad value {k}: {v/len(df)*100}%" for k, v in bad.items())
        + "\n",
    )

    result_text.insert(tk.END, f"{ones}")

    result_text.config(state=tk.DISABLED)


# Создаем главное окно
root = tk.Tk()
root.title("Tkinter Interface")

# Строка 1: Текстовое поле
input_label = tk.Label(root, text="Input")
input_label.grid(row=0, column=2, sticky=tk.W)
input_entry = tk.Entry(root)
input_entry.grid(row=0, column=4, padx=10, pady=5)

# Строка 2: Чекбоксы
checkboxes_vars = {}
for i, col in enumerate(cols):
    checkbox_var = tk.IntVar()
    checkboxes_vars[col] = checkbox_var
    checkbox = tk.Checkbutton(root, text=col, variable=checkbox_var)
    checkbox.grid(row=1, column=i, padx=5, pady=5)

# Строка 3: Кнопка "Run"
run_button = tk.Button(root, text="Run", command=run_function)
run_button.grid(row=2, column=0, columnspan=7, pady=10)

# Строка 4: Область для вывода результата
result_text = tk.Text(root, height=20, width=100, state=tk.DISABLED)
result_text.grid(row=3, column=0, columnspan=7, padx=10, pady=5)

# Запускаем главный цикл событий
root.mainloop()
