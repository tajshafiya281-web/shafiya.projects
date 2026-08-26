import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ---------------- DATABASE ----------------

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")

conn.commit()


# ---------------- FUNCTIONS ----------------

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if date == "" or category == "" or amount == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill Date, Category and Amount"
        )
        return

    try:
        amount = float(amount)

        cursor.execute(
            "INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
            (date, category, amount, description)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Expense added successfully!"
        )

        clear_fields()
        show_expenses()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid amount"
        )


def show_expenses():

    # Remove old data from table
    for item in expense_table.get_children():
        expense_table.delete(item)

    cursor.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    )

    expenses = cursor.fetchall()

    total = 0

    for expense in expenses:

        expense_table.insert(
            "",
            tk.END,
            values=expense
        )

        total += expense[3]

    total_label.config(
        text=f"Total Expenses: ₹{total:.2f}"
    )


def delete_expense():

    selected = expense_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select an expense to delete"
        )
        return

    item = expense_table.item(selected[0])

    expense_id = item["values"][0]

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    conn.commit()

    messagebox.showinfo(
        "Deleted",
        "Expense deleted successfully!"
    )

    show_expenses()


def clear_fields():

    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)


# ---------------- GUI WINDOW ----------------

root = tk.Tk()

root.title("Daily Expense Tracker")

root.geometry("850x600")

root.configure(bg="#f2f2f2")


# ---------------- TITLE ----------------

title_label = tk.Label(
    root,
    text="💰 DAILY EXPENSE TRACKER",
    font=("Arial", 20, "bold"),
    bg="#f2f2f2"
)

title_label.pack(pady=15)


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

input_frame.pack(pady=10)


# Date

tk.Label(
    input_frame,
    text="Date:",
    font=("Arial", 12),
    bg="#f2f2f2"
).grid(row=0, column=0, padx=10, pady=10)

date_entry = tk.Entry(
    input_frame,
    width=20
)

date_entry.grid(
    row=0,
    column=1
)


# Category

tk.Label(
    input_frame,
    text="Category:",
    font=("Arial", 12),
    bg="#f2f2f2"
).grid(row=0, column=2, padx=10)

category_entry = tk.Entry(
    input_frame,
    width=20
)

category_entry.grid(
    row=0,
    column=3
)


# Amount

tk.Label(
    input_frame,
    text="Amount (₹):",
    font=("Arial", 12),
    bg="#f2f2f2"
).grid(row=1, column=0, padx=10, pady=10)

amount_entry = tk.Entry(
    input_frame,
    width=20
)

amount_entry.grid(
    row=1,
    column=1
)


# Description

tk.Label(
    input_frame,
    text="Description:",
    font=("Arial", 12),
    bg="#f2f2f2"
).grid(row=1, column=2, padx=10)

description_entry = tk.Entry(
    input_frame,
    width=20
)

description_entry.grid(
    row=1,
    column=3
)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

button_frame.pack(pady=10)


add_button = tk.Button(
    button_frame,
    text="Add Expense",
    font=("Arial", 11, "bold"),
    width=15,
    command=add_expense
)

add_button.grid(
    row=0,
    column=0,
    padx=10
)


delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    font=("Arial", 11, "bold"),
    width=15,
    command=delete_expense
)

delete_button.grid(
    row=0,
    column=1,
    padx=10
)


# ---------------- EXPENSE TABLE ----------------

columns = (
    "ID",
    "Date",
    "Category",
    "Amount",
    "Description"
)

expense_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=12
)


for column in columns:
    expense_table.heading(
        column,
        text=column
    )

    expense_table.column(
        column,
        width=150
    )


expense_table.pack(
    padx=20,
    pady=15,
    fill="both",
    expand=True
)


# ---------------- TOTAL ----------------

total_label = tk.Label(
    root,
    text="Total Expenses: ₹0.00",
    font=("Arial", 16, "bold"),
    bg="#f2f2f2"
)

total_label.pack(
    pady=10
)


# ---------------- LOAD DATA ----------------

show_expenses()


# ---------------- RUN PROGRAM ----------------

root.mainloop()


# Close database when program ends
conn.close()