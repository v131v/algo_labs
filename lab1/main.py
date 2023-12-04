import tkinter as tk
from compute import *
from tkinter import messagebox

if __name__ == "__main__":
    
    # Создание основного окна
    root = tk.Tk()
    root.title("Dataset generator")

    output_frame = tk.Frame(root)
    output_frame.pack(side=tk.TOP, padx=10)
    
    output_label = tk.Label(output_frame, text="Output filename")
    output_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

    output_entry = tk.Entry(output_frame)
    output_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    
    
    compute_frame = tk.Frame(root)
    compute_frame.pack(side=tk.BOTTOM, padx=10)
    
    count_label = tk.Label(compute_frame, text="Count")
    count_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

    count_entry = tk.Entry(compute_frame)
    count_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    # Первый столбец
    column1_frame = tk.Frame(root)
    column1_frame.pack(side=tk.LEFT, padx=10)

    a_label = tk.Label(column1_frame, text="Sberbank, %")
    a_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    a_entry = tk.Entry(column1_frame)
    a_entry.grid(row=0, column=1, padx=5, pady=5)

    b_label = tk.Label(column1_frame, text="Tinkoff, %")
    b_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    b_entry = tk.Entry(column1_frame)
    b_entry.grid(row=1, column=1, padx=5, pady=5)

    c_label = tk.Label(column1_frame, text="VTB, %")
    c_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    c_entry = tk.Entry(column1_frame)
    c_entry.grid(row=2, column=1, padx=5, pady=5)

    d_label = tk.Label(column1_frame, text="Alpha-bank, %")
    d_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
    d_entry = tk.Entry(column1_frame)
    d_entry.grid(row=3, column=1, padx=5, pady=5)

    # Второй столбец
    column2_frame = tk.Frame(root)
    column2_frame.pack(side=tk.LEFT, padx=10)

    x_label = tk.Label(column2_frame, text="Mastercard, %")
    x_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    x_entry = tk.Entry(column2_frame)
    x_entry.grid(row=0, column=1, padx=5, pady=5)

    y_label = tk.Label(column2_frame, text="Visa, %")
    y_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    y_entry = tk.Entry(column2_frame)
    y_entry.grid(row=1, column=1, padx=5, pady=5)

    z_label = tk.Label(column2_frame, text="Mir, %")
    z_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    z_entry = tk.Entry(column2_frame)
    z_entry.grid(row=2, column=1, padx=5, pady=5)
    
    def handler():
        banks_p = {
            "sberbank": int(a_entry.get()),
            "tinkoff": int(b_entry.get()),
            "vtb": int(c_entry.get()),
            "alphabank": int(d_entry.get()),
        }
        s = 0
        for key in banks_p:
            s += banks_p[key]
        if s != 100:
            messagebox.showinfo("Error", "Sum of banks probabilities != 100")
            return
        
        systems_p = {
            "mastercard": int(x_entry.get()),
            "visa": int(y_entry.get()),
            "mir": int(z_entry.get()),
        }
        s = 0
        for key in systems_p:
            s += systems_p[key]
        if s != 100:
            messagebox.showinfo("Error", "Sum of payment systems probabilities != 100")
            return
        
        compute(int(count_entry.get()), output_entry.get(), banks_p, systems_p)
        messagebox.showinfo("Success", "Dataset saved")
    
    # Кнопка для выполнения операции (вашего выбора)
    calculate_button = tk.Button(compute_frame, text="Compute", command=handler)
    calculate_button.grid(row=2, columnspan=2, pady=10)

    # Запуск цикла обработки событий
    root.mainloop()
        
