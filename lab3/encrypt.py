import hashlib
from tkinter import Tk, Label, Button, filedialog, StringVar, OptionMenu, Entry


def encrypt_numbers(file_path, algorithm, salt_option):
    with open(file_path, "r") as file:
        numbers = file.readlines()

    output = ""

    for number in numbers:
        number = number.strip()

        if salt_option == "No Salt":
            salt = ""
        elif salt_option == "Numeric Salt":
            salt = "123"
        elif salt_option == "Alphabetic Salt":
            salt = "abc"

        if salt:
            number += salt

        if algorithm == "MD5":
            encrypted = hashlib.md5(number.encode()).hexdigest()
        elif algorithm == "SHA1":
            encrypted = hashlib.sha1(number.encode()).hexdigest()
        elif algorithm == "SHA256":
            encrypted = hashlib.sha256(number.encode()).hexdigest()

        output += f"{encrypted}\n"

    with open(f"encrypted_numbers_{algorithm.lower()}.txt", "w") as output_file:
        output_file.write(output)


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        selected_algorithm = algorithm_var.get()
        selected_salt_option = salt_option_var.get()
        encrypt_numbers(file_path, selected_algorithm, selected_salt_option)
        status_label.config(text="Encryption completed. Check 'encrypted_numbers.txt'")


root = Tk()
root.title("Phone Number Encryption")

algorithms = ["MD5", "SHA1", "SHA256"]

salt_options = ["No Salt", "Numeric Salt", "Alphabetic Salt"]

algorithm_var = StringVar(root)
algorithm_var.set(algorithms[0])

algorithm_menu = OptionMenu(root, algorithm_var, *algorithms)
algorithm_menu.pack(pady=10)

salt_option_var = StringVar(root)
salt_option_var.set(salt_options[0])

salt_option_menu = OptionMenu(root, salt_option_var, *salt_options)
salt_option_menu.pack(pady=10)

browse_button = Button(root, text="Select File", command=browse_file)
browse_button.pack(pady=10)

status_label = Label(root, text="")
status_label.pack()

root.mainloop()
