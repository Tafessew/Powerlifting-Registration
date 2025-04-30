# view.py
# Wada Tafesse
# 4.30.2025
# GUI for registering powerlifters and viewing roster info.

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import subprocess
import platform
from model import Lifter, LifterManager

manager = LifterManager()

# new window to enter attempts
def open_attempts_page(lifter):
    attempts_window = tk.Toplevel()
    attempts_window.title("Enter Attempts")
    attempts_window.geometry("300x400")

    tk.Label(attempts_window, text="Squat (kg):").pack(pady=5)
    squat_entry = tk.Entry(attempts_window)
    squat_entry.pack(pady=5)

    tk.Label(attempts_window, text="Bench (kg):").pack(pady=5)
    bench_entry = tk.Entry(attempts_window)
    bench_entry.pack(pady=5)

    tk.Label(attempts_window, text="Deadlift (kg):").pack(pady=5)
    deadlift_entry = tk.Entry(attempts_window)
    deadlift_entry.pack(pady=5)

    def save_attempts():
        lifter.squat = squat_entry.get()
        lifter.bench = bench_entry.get()
        lifter.deadlift = deadlift_entry.get()
        manager.save_lifter_to_csv(lifter)
        messagebox.showinfo("Success", "Successfully Registered!")
        attempts_window.destroy()

    tk.Button(attempts_window, text="Submit Attempts", command=save_attempts).pack(pady=20)

# Handles form submission
def submit_form():
    name = name_entry.get()
    gender = gender_var.get()
    weight_class = weight_class_var.get()
    division = division_var.get()

    if not name or not gender or not weight_class or not division:
        messagebox.showerror("Error", "Please fill out all fields.")
        return

    lifter = Lifter(name, gender, weight_class, division, "", "", "")
    open_attempts_page(lifter)
    clear_form()

# Resets form fields
def clear_form():
    name_entry.delete(0, tk.END)
    gender_var.set("Male")
    weight_class_var.set(weight_classes[0])
    division_var.set("Raw")

# Displays all registered lifters
def show_roster():
    roster_window = tk.Toplevel()
    roster_window.title("Roster")
    roster_window.geometry("400x500")

    for lifter in manager.lifters:
        text = f"{lifter.name} | {lifter.gender} | {lifter.weight_class} | {lifter.division} | {lifter.squat} | {lifter.bench} | {lifter.deadlift}"
        tk.Label(roster_window, text=text, anchor="w", justify="left").pack(pady=2)

# Opens CSV or TXT files
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        if file_path.endswith(".csv"):
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        else:
            with open(file_path, "r") as f:
                content = f.read()
            file_window = tk.Toplevel()
            file_window.title("Opened File")
            text_area = tk.Text(file_window, wrap=tk.WORD, height=30, width=60)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, content)
            text_area.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Powerlifting Meet Registration")
root.geometry("300x550")

# Menubar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Roster", command=show_roster)
file_menu.add_command(label="Exit", command=root.destroy)
menu_bar.add_cascade(label="Menu", menu=file_menu)

open_menu = tk.Menu(menu_bar, tearoff=0)
open_menu.add_command(label="CSV", command=open_file)
menu_bar.add_cascade(label="Open", menu=open_menu)
root.config(menu=menu_bar)

# Form
tk.Label(root, text="Name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Gender:").pack(pady=5)
gender_var = tk.StringVar(value="Male")
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male").pack()
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female").pack()

tk.Label(root, text="Weight Class:").pack(pady=5)
weight_classes = ["43 kg", "47 kg", "52 kg", "57 kg", "63 kg", "69 kg", "76 kg", "84 kg", "84+ kg"]
weight_class_var = tk.StringVar(value=weight_classes[0])
ttk.Combobox(root, textvariable=weight_class_var, values=weight_classes, state="readonly").pack(pady=5)

tk.Label(root, text="Division Type:").pack(pady=5)
division_var = tk.StringVar(value="Raw")
tk.Radiobutton(root, text="Raw", variable=division_var, value="Raw").pack()
tk.Radiobutton(root, text="Equipped", variable=division_var, value="Equipped").pack()

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)
tk.Button(button_frame, text="Submit", command=submit_form).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Clear", command=clear_form).pack(side=tk.LEFT, padx=10)

root.mainloop()
