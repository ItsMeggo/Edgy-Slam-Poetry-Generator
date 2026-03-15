import os
import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook


def load_endings():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, 'Shadow-the-Hedgehog-Engings-List.xlsx')
    book = load_workbook(excel_path)
    sheet = book.active
    rows = sheet.rows
    next(rows)  # skip header row
    all_rows = []
    for row in rows:
        for cell in row:
            all_rows.append(cell.value)
    return all_rows


def generate_poem():
    try:
        line1 = int(entry1.get())
        line2 = int(entry2.get())
        line3 = int(entry3.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid whole numbers.")
        return

    if not (1 <= line1 <= 326) or not (1 <= line2 <= 326) or not (1 <= line3 <= 326):
        messagebox.showerror("Invalid Input", "Please enter numbers between 1 and 326.")
        return

    poem_line_1 = endings[line1 - 1]
    poem_line_2 = endings[line2 - 1]
    poem_line_3 = endings[line3 - 1]

    poem_text.config(state='normal')
    poem_text.delete(1.0, tk.END)
    poem_text.insert(tk.END, f"{poem_line_1}\n{poem_line_2}\n{poem_line_3}")
    poem_text.config(state='disabled')


# Load data
try:
    endings = load_endings()
except Exception as exc:
    import sys
    # Show a simple error message before the main window opens
    _root = tk.Tk()
    _root.withdraw()
    messagebox.showerror(
        "Startup Error",
        f"Could not load endings data:\n{exc}\n\n"
        "Make sure 'Shadow-the-Hedgehog-Engings-List.xlsx' is in the same folder as Main.py.",
    )
    _root.destroy()
    sys.exit(1)

# Build the GUI
root = tk.Tk()
root.title("Edgy Slam Poetry Generator")
root.geometry("520x380")
root.resizable(False, False)

# Title
tk.Label(
    root,
    text="\U0001f3ad Edgy Slam Poetry Generator",
    font=("Helvetica", 16, "bold"),
).pack(pady=(16, 2))

tk.Label(
    root,
    text="Based on the Shadow the Hedgehog game endings",
    font=("Helvetica", 10),
    fg="#555555",
).pack()

# Input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=18)

labels = [
    "Pick your favourite number (1\u2013326):",
    "Pick your least favourite number (1\u2013326):",
    "Pick the number you least care about (1\u2013326):",
]
entries = []
for i, text in enumerate(labels):
    tk.Label(input_frame, text=text, anchor="w").grid(
        row=i, column=0, sticky="w", pady=4, padx=(0, 8)
    )
    spinbox = tk.Spinbox(input_frame, from_=1, to=326, width=8, font=("Helvetica", 11))
    spinbox.grid(row=i, column=1)
    entries.append(spinbox)

entry1, entry2, entry3 = entries

# Generate button
tk.Button(
    root,
    text="Generate Poem!",
    command=generate_poem,
    bg="#4a4a8a",
    fg="white",
    font=("Helvetica", 12, "bold"),
    padx=20,
    pady=6,
    relief="flat",
    cursor="hand2",
).pack(pady=(0, 12))

# Poem output area
poem_frame = tk.LabelFrame(
    root,
    text="Your Poem",
    font=("Helvetica", 11, "bold"),
    padx=10,
    pady=8,
)
poem_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

poem_text = tk.Text(
    poem_frame,
    height=4,
    wrap="word",
    font=("Georgia", 11, "italic"),
    state='disabled',
    bg="#f7f7f7",
    relief="flat",
)
poem_text.pack(fill="both", expand=True)

root.mainloop()
