import os
import random
import threading
import tkinter as tk
from tkinter import messagebox, ttk
from openpyxl import load_workbook

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ── Shadow the Hedgehog colour palette ──────────────────────────────────────
BG       = "#0a0a0a"   # near-black background
FG       = "#e8e8e8"   # off-white text
RED      = "#cc0000"   # Shadow red
DARK_RED = "#8b0000"   # darker red for hover / secondary buttons
MUTED    = "#888888"   # muted label text
ENTRY_BG = "#1c1c1c"   # dark entry / text-area background
FRAME_BG = "#111111"   # slightly lighter frame background

# ── Font constants ───────────────────────────────────────────────────────────
FONT_TITLE  = ("Helvetica", 17, "bold")
FONT_BOLD   = ("Helvetica", 11, "bold")
FONT_NORMAL = ("Helvetica", 10)
FONT_SMALL  = ("Helvetica", 9)
FONT_SPIN   = ("Helvetica", 11)
FONT_POEM   = ("Georgia", 11, "italic")
FONT_TAB    = ("Helvetica", 10, "bold")

# ── Personal-poem questions ──────────────────────────────────────────────────
QUESTIONS = [
    "What is your star sign?  (e.g. Aries)",
    "What is your biggest fear?",
    "Name a weapon or power you\u2019d wield in battle:",
]


def load_endings():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(script_dir, "Shadow-the-Hedgehog-Engings-List.xlsx")
    book = load_workbook(excel_path)
    sheet = book.active
    rows = sheet.rows
    next(rows)  # skip header row
    all_rows = []
    for row in rows:
        for cell in row:
            all_rows.append(cell.value)
    return all_rows


def letters_to_number(text: str) -> int:
    """Sum the alphabetic position (a=1 … z=26) of every letter in *text*,
    then map the total to the range 1–326."""
    total = sum(ord(c) - ord("a") + 1 for c in text.lower() if c.isalpha())
    if total == 0:
        return 1
    return (total - 1) % 326 + 1


def _display_poem(line1: str, line2: str, line3: str):
    poem_text.config(state="normal")
    poem_text.delete(1.0, tk.END)
    poem_text.insert(tk.END, f"{line1}\n{line2}\n{line3}")
    poem_text.config(state="disabled")


def generate_poem():
    try:
        n1 = int(entry1.get())
        n2 = int(entry2.get())
        n3 = int(entry3.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid whole numbers.")
        return

    if not (1 <= n1 <= 326) or not (1 <= n2 <= 326) or not (1 <= n3 <= 326):
        messagebox.showerror("Invalid Input", "Please enter numbers between 1 and 326.")
        return

    _display_poem(endings[n1 - 1], endings[n2 - 1], endings[n3 - 1])


def randomise_poem():
    """Fill all three spinboxes with random values and immediately generate the poem."""
    for sp in (entry1, entry2, entry3):
        sp.delete(0, tk.END)
        sp.insert(0, str(random.randint(1, 326)))
    generate_poem()


def generate_personal_poem():
    """Convert each personal answer to a number via letter positions and build the poem."""
    answers = [e.get().strip() for e in personal_entries]
    if any(a == "" for a in answers):
        messagebox.showerror("Missing Answer", "Please answer all three questions.")
        return
    nums = [letters_to_number(a) for a in answers]
    _display_poem(endings[nums[0] - 1], endings[nums[1] - 1], endings[nums[2] - 1])


def _speak(text: str):
    """Run TTS in a daemon thread so the GUI stays responsive."""
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 115)   # slow, dramatic delivery
        engine.say(text)
        engine.runAndWait()
    except Exception as exc:
        root.after(0, lambda: messagebox.showerror(
            "TTS Error",
            f"Could not read the poem aloud:\n{exc}",
        ))


def read_poem():
    poem_content = poem_text.get(1.0, tk.END).strip()
    if not poem_content:
        messagebox.showinfo("No Poem", "Generate a poem first!")
        return
    if not TTS_AVAILABLE:
        messagebox.showinfo(
            "TTS Unavailable",
            "Text-to-speech is not installed.\nRun:  pip install pyttsx3",
        )
        return
    threading.Thread(target=_speak, args=(poem_content,), daemon=True).start()


# ── Load data ────────────────────────────────────────────────────────────────
try:
    endings = load_endings()
except Exception as exc:
    import sys
    _root = tk.Tk()
    _root.withdraw()
    messagebox.showerror(
        "Startup Error",
        f"Could not load endings data:\n{exc}\n\n"
        "Make sure 'Shadow-the-Hedgehog-Engings-List.xlsx' is in the same folder as Main.py.",
    )
    _root.destroy()
    sys.exit(1)

# ── Build GUI ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Edgy Slam Poetry Generator")
root.geometry("580x570")
root.resizable(False, False)
root.configure(bg=BG)

# ── ttk style (for Notebook tabs) ────────────────────────────────────────────
style = ttk.Style(root)
style.theme_use("clam")
style.configure(".", background=BG, foreground=FG)
style.configure("TNotebook", background=BG, bordercolor=RED, tabmargins=[2, 2, 2, 0])
style.configure(
    "TNotebook.Tab",
    background=DARK_RED,
    foreground=FG,
    padding=[12, 4],
    font=FONT_TAB,
)
style.map(
    "TNotebook.Tab",
    background=[("selected", RED)],
    foreground=[("selected", "#ffffff")],
)
style.configure("TFrame", background=BG)


# ── Helper factories ─────────────────────────────────────────────────────────
def make_label(parent, text, **kw):
    kw.setdefault("bg", BG)
    kw.setdefault("fg", FG)
    return tk.Label(parent, text=text, **kw)


def make_button(parent, text, cmd, **kw):
    kw.setdefault("bg", RED)
    kw.setdefault("fg", "#ffffff")
    kw.setdefault("activebackground", DARK_RED)
    kw.setdefault("activeforeground", "#ffffff")
    kw.setdefault("font", FONT_BOLD)
    kw.setdefault("relief", "flat")
    kw.setdefault("cursor", "hand2")
    kw.setdefault("padx", 16)
    kw.setdefault("pady", 5)
    return tk.Button(parent, text=text, command=cmd, **kw)


# ── Header ───────────────────────────────────────────────────────────────────
make_label(
    root,
    "\U0001f3ad  Edgy Slam Poetry Generator",
    font=FONT_TITLE,
    fg=RED,
).pack(pady=(14, 2))

make_label(
    root,
    "Based on the Shadow the Hedgehog game endings",
    font=FONT_NORMAL,
    fg=MUTED,
).pack()

# ── Notebook tabs ─────────────────────────────────────────────────────────────
nb = ttk.Notebook(root)
nb.pack(fill="both", padx=16, pady=(10, 0))

# ── TAB 1 – Manual / Random ──────────────────────────────────────────────────
tab1 = tk.Frame(nb, bg=BG)
nb.add(tab1, text="  \U0001f3b2  Manual / Random  ")

input_frame = tk.Frame(tab1, bg=BG)
input_frame.pack(pady=12)

spin_labels = [
    "Pick your favourite number (1\u2013326):",
    "Pick your least favourite number (1\u2013326):",
    "Pick the number you least care about (1\u2013326):",
]
entries = []
for i, text in enumerate(spin_labels):
    make_label(input_frame, text, anchor="w").grid(
        row=i, column=0, sticky="w", pady=4, padx=(0, 8)
    )
    sp = tk.Spinbox(
        input_frame,
        from_=1,
        to=326,
        width=8,
        font=FONT_SPIN,
        bg=ENTRY_BG,
        fg=FG,
        buttonbackground=RED,
        insertbackground=FG,
        relief="flat",
    )
    sp.grid(row=i, column=1)
    entries.append(sp)

entry1, entry2, entry3 = entries

btn_row1 = tk.Frame(tab1, bg=BG)
btn_row1.pack(pady=(4, 10))
make_button(btn_row1, "\u2699\ufe0f  Generate Poem!", generate_poem).pack(side="left", padx=6)
make_button(btn_row1, "\U0001f3b2  Randomise!", randomise_poem, bg=DARK_RED).pack(side="left", padx=6)

# ── TAB 2 – Personal Poem ────────────────────────────────────────────────────
tab2 = tk.Frame(nb, bg=BG)
nb.add(tab2, text="  \U0001f52e  Personal Poem  ")

make_label(
    tab2,
    "Answer the questions \u2014 your replies shape the poem.",
    font=FONT_SMALL,
    fg=MUTED,
).pack(pady=(8, 4))

pq_frame = tk.Frame(tab2, bg=BG)
pq_frame.pack(pady=4, padx=16, fill="x")

personal_entries = []
for i, q in enumerate(QUESTIONS):
    make_label(pq_frame, q, anchor="w", font=FONT_NORMAL).grid(
        row=i, column=0, sticky="w", pady=5, padx=(0, 8)
    )
    ent = tk.Entry(
        pq_frame,
        width=24,
        bg=ENTRY_BG,
        fg=FG,
        insertbackground=FG,
        relief="flat",
        font=FONT_SPIN,
    )
    ent.grid(row=i, column=1, sticky="w")
    personal_entries.append(ent)

make_button(tab2, "\U0001f52e  Generate My Personal Poem!", generate_personal_poem).pack(
    pady=(8, 10)
)

# ── Poem output ──────────────────────────────────────────────────────────────
poem_lf = tk.LabelFrame(
    root,
    text=" Your Poem ",
    font=FONT_BOLD,
    bg=FRAME_BG,
    fg=RED,
    bd=2,
    relief="ridge",
    padx=10,
    pady=8,
)
poem_lf.pack(fill="both", expand=True, padx=16, pady=(8, 4))

poem_text = tk.Text(
    poem_lf,
    height=4,
    wrap="word",
    font=FONT_POEM,
    state="disabled",
    bg=ENTRY_BG,
    fg=FG,
    relief="flat",
    insertbackground=FG,
)
poem_text.pack(fill="both", expand=True)

# ── Read-poem button ──────────────────────────────────────────────────────────
make_button(root, "\U0001f50a  Read the Poem!", read_poem, bg=DARK_RED).pack(pady=(4, 14))

root.mainloop()
