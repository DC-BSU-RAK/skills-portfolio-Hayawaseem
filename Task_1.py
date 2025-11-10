from tkinter import *   # Import tkinter for GUI
from tkinter import messagebox  # Import messagebox 
import random, math, os # It is used for when the file exists or not 

SOUNDS_AVAILABLE = False  # Flag to check if pygame is installed
click_sound = correct_sound = wrong_sound = countdown_sound = None  # Sound variables

try:
    import pygame
    pygame.mixer.init()  # Initialize the mixer for sound
    SOUNDS_AVAILABLE = True  # Enable sound support
except:
    pass  # Ignore errors if pygame not installed

# Function to load a sound file
def load_sound(path):
    if not SOUNDS_AVAILABLE:
        return None
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

# Load sound effects
click_sound = load_sound("click.wav")
correct_sound = load_sound("correct.wav")
wrong_sound = load_sound("wrong.wav")
countdown_sound = load_sound("countdown.wav")

# Play a sound if available
def play(snd):
    if snd != None:
        if SOUNDS_AVAILABLE:
            try:
                snd.play()
            except:
                pass

# Play background countdown sound continuously
def play_countdown():
    if countdown_sound != None:
        if SOUNDS_AVAILABLE:
            countdown_sound.play(loops=-1)

# Stop the countdown sound
def stop_countdown():
    if countdown_sound != None:
        if SOUNDS_AVAILABLE:
            countdown_sound.stop()

root = Tk()  # Create main Tkinter window
root.iconbitmap('math_quiz.ico') # For icon 
root.title("Math Quiz")  # Set window title
root.geometry("960x540")  # Set window size (big window)
root.config(bg="#050317")  # Set background color
root.resizable(False, False)  # Disable resizing

# Variables
score = 0
question_num = 0
difficulty = 0
tries = 0
first_number = 0
second_number = 0
answer = 0

# Theme Colors
theme = {}
theme["bg"] = "#050317"
theme["card_bg"] = "#0d0b16"
theme["primary"] = "#00f5ff"
theme["accent"] = "#ff4dd2"
theme["muted"] = "#99a0b8"
theme["particle1"] = "#00f5ff"
theme["particle2"] = "#ff4dd2"
theme["particle3"] = "#7c5cff"

# Background Canvas 
bg = Canvas(root, width=960, height=540, bg=theme["bg"], highlightthickness=0)
bg.pack(fill="both", expand=True)

# Starfield 
stars = []
i = 0
while i < 120:  # More stars to fill bigger window
    x = random.randint(0, 960)
    y = random.randint(0, 540)
    size = random.randint(1, 3)
    color = random.choice([theme["primary"], theme["accent"], "#bfefff", "#ffd6f0"])
    star = bg.create_oval(x, y, x + size, y + size, fill=color, outline="")
    stars.append({"id": star, "x": x, "y": y, "size": size, "speed": random.uniform(0.1, 0.3)})
    i += 1

# Function to move stars downward 
def move_stars():
    for s in stars:
        s["y"] += s["speed"]
        if s["y"] > 540:
            s["y"] = 0
            s["x"] = random.randint(0, 960)
        bg.coords(s["id"], s["x"], s["y"], s["x"] + s["size"], s["y"] + s["size"])
    root.after(50, move_stars)

move_stars()

# Floating particles
particles = []
i = 0
while i < 40:  # More particles for bigger window
    x = random.randint(0, 960)
    y = random.randint(0, 540)
    size = random.randint(8, 14)
    color = random.choice([theme["particle1"], theme["particle2"], theme["particle3"]])
    p = bg.create_oval(x, y, x + size, y + size, fill=color, outline="")
    particles.append({"id": p, "x": x, "y": y, "size": size, "dx": random.uniform(-0.3, 0.3), "dy": random.uniform(-0.3, 0.3)})
    i += 1

# Animate particles 
def move_particles():
    for p in particles:
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        if p["x"] < 0 or p["x"] + p["size"] > 960:
            p["dx"] = -p["dx"]
        if p["y"] < 0 or p["y"] + p["size"] > 540:
            p["dy"] = -p["dy"]
        bg.coords(p["id"], p["x"], p["y"], p["x"] + p["size"], p["y"] + p["size"])
    root.after(50, move_particles)

move_particles()

# Helper function
def clear():
    for w in root.winfo_children():
        if w != bg:
            w.destroy()

# Button with hover effect
def glass_button(master, text, cmd, width=180, height=50):
    def wrapped_cmd():
        play(click_sound)
        stop_countdown()
        try:
            cmd()
        except:
            try:
                cmd(None)
            except:
                pass
    b = Button(master, text=text, command=wrapped_cmd, font=("Consolas", 14, "bold"),
               fg="white", bg=theme["primary"], activebackground=theme["accent"],
               activeforeground="white", bd=0, relief="flat", padx=12, pady=6, width=12)
    b.bind("<Enter>", lambda e: b.config(bg=theme["accent"]))
    b.bind("<Leave>", lambda e: b.config(bg=theme["primary"]))
    return b

# Entry box with neon focus effect
def glass_entry(master):
    e = Entry(master, font=("Consolas", 16), width=8, justify="center", bg="#091021",
              fg="white", bd=2, relief="ridge", insertbackground="white")
    e.bind("<FocusIn>", lambda ev: e.config(bg="#07102a"))
    e.bind("<FocusOut>", lambda ev: e.config(bg="#091021"))
    return e

# --- GAME LOGIC ---
def random_int():
    if difficulty == 1:
        return random.randint(1, 9)
    elif difficulty == 2:
        return random.randint(10, 99)
    else:
        return random.randint(100, 999)

def decide_operation():
    if random.random() < 0.5:
        return "+"
    else:
        return "-"

def display_problem():
    global first_number, second_number, answer, tries
    first_number = random_int()
    second_number = random_int()
    op = decide_operation()
    if op == "-" and first_number < second_number:
        first_number, second_number = second_number, first_number
    if op == "+":
        answer = first_number + second_number
    else:
        answer = first_number - second_number
    tries = 0
    show_question(op)

def start(level):
    global difficulty, score, question_num
    difficulty = level
    score = 0
    question_num = 0
    next_question()

def next_question():
    global question_num
    question_num += 1
    if question_num > 10:
        display_results()
    else:
        display_problem()

def show_question(op):
    clear()
    card = Frame(root, bg=theme["card_bg"], bd=3, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=300)
    Label(card, text=f"Question {question_num}/10   |   Score: {score}", fg=theme["accent"],
          bg=theme["card_bg"], font=("Consolas", 14)).pack(pady=10)
    Label(card, text=f"{first_number} {op} {second_number} = ?", fg=theme["primary"],
          bg=theme["card_bg"], font=("Consolas", 26, "bold")).pack(pady=15)
    entry = glass_entry(card)
    entry.pack(pady=10)
    entry.focus()
    btn_frame = Frame(card, bg=theme["card_bg"])
    btn_frame.pack(pady=10)
    glass_button(btn_frame, "Submit", lambda: check(entry)).pack(side=LEFT, padx=8)
    glass_button(btn_frame, "Back", start_screen).pack(side=LEFT, padx=8)
    root.bind("<Return>", lambda e: (play(click_sound), check(entry)))
    play_countdown()

def check(entry):
    global score, tries
    try:
        ans = int(entry.get())
    except:
        play(wrong_sound)
        messagebox.showerror("Error", "Enter numbers only!")
        entry.delete(0, END)
        return
    if ans == answer:
        stop_countdown()
        points = 10 if tries == 0 else 5
        score += points
        play(correct_sound)
        messagebox.showinfo("Correct!", f"+{points} points")
        next_question()
    else:
        tries += 1
        play(wrong_sound)
        if tries == 1:
            stop_countdown()
            messagebox.showerror("Wrong", "Try again!")
            play_countdown()
            entry.delete(0, END)
        else:
            stop_countdown()
            messagebox.showerror("Wrong", f"The correct answer was {answer}")
            next_question()

def display_results():
    clear()
    grade = "F"
    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    elif score >= 50: grade = "D"
    card = Frame(root, bg=theme["card_bg"], bd=3, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=220)
    Label(card, text=f"Final Score: {score}/100\nGrade: {grade}", fg=theme["primary"],
          bg=theme["card_bg"], font=("Consolas", 20, "bold")).pack(pady=30)
    glass_button(card, "Play Again", start_screen).pack()

# --- NEW: INSTRUCTION SCREEN ---
def display_instructions():
    clear()
    stop_countdown()
    card = Frame(root, bg=theme["card_bg"], bd=3, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=600, height=340)
    Label(card, text="📘 Instructions", fg=theme["accent"], bg=theme["card_bg"],
          font=("Consolas", 22, "bold")).pack(pady=10)
    Label(card, text="1 Choose a difficulty level.\n\n"
                     "2 Solve 10 math questions.\n\n"
                     "3 Each correct answer gives points.\n\n"
                     "4 Try to score the highest grade!",
          fg="white", bg=theme["card_bg"], font=("Consolas", 14), justify="center").pack(pady=10)
    glass_button(card, "Continue →", display_menu).pack(pady=15)

def display_menu():
    clear()
    stop_countdown()
    card = Frame(root, bg=theme["card_bg"], bd=3, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)
    Label(card, text="Select Difficulty", fg=theme["accent"], bg=theme["card_bg"],
          font=("Consolas", 18, "bold")).pack(pady=20)
    glass_button(card, "Easy", lambda: start(1), width=20).pack(pady=10)
    glass_button(card, "Moderate", lambda: start(2), width=20).pack(pady=10)
    glass_button(card, "Advanced", lambda: start(3), width=20).pack(pady=10)

def start_screen():
    clear()
    stop_countdown()
    Label(root, text="Math Quiz", fg=theme["primary"], bg=theme["bg"],
          font=("Orbitron", 36, "bold")).place(relx=0.5, rely=0.3, anchor="center")
    glass_button(root, "Start Quiz", display_instructions).place(relx=0.5, rely=0.55, anchor="center")

# Launch start screen
start_screen()
root.mainloop()