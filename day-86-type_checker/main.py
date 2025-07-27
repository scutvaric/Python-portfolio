from tkinter import *
from tkinter import messagebox
import math
from random import shuffle

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
LENGTH_IN_MIN = 1
timer = None
i = -1
score=0
words_to_type = []
labels = []

def create_words():
    global words_to_type

    for label in labels:
        label.destroy()
    labels.clear()

    for index in range(3):
        label = Label(text="", font=(FONT_NAME, 12), bg=YELLOW)
        label.grid(column=index, row=2)
        labels.append(label)

    labels[1].config(fg="red", font=(FONT_NAME, 12, "bold"))

    with open("data.txt", "r") as file:
        content = file.read()
        words_list = [word.strip() for word in content.split(",")]

    words_to_type = words_list[:]
    shuffle(words_to_type)


def next_word():
    global words_to_type, i
    i += 1
    for index, label in enumerate(labels):
        if i + index < len(words_to_type):
            label.config(text=words_to_type[i+index])
        else:
            label.config(text="Out of words")

def check_typing(event=None):
    global score
    if user_input.get() == "":
        pass
    elif user_input.get() == labels[1].cget("text"):
        score += 1
        next_word()
        update_title()
        user_input.delete(0, END)


def update_title():
    window.title(f"How many words can you type in a minute? Current score: {score}")


# ---------------------------- TIMER RESET ------------------------------- #

def start_game():
    start_button.config(state="disabled")

def reset_timer():
    global score
    score=0
    start_button.config(state="normal")
    update_title()
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    create_words()


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    start_game()
    create_words()
    next_word()
    length_in_sec = LENGTH_IN_MIN * 60
    count_down(length_in_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        messagebox.showinfo(message=f"Congrats, you have typed {score} words in 1 minute! ")
        reset_timer()



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
update_title()
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=120, height=50, bg=YELLOW, highlightthickness=0)
timer_text = canvas.create_text(60, 25, text="00:00", fill="black", font=(FONT_NAME, 35,"bold"))
canvas.grid(column=1, row=0)


instruction_text = Label(text="↓Type the word in red below↓", bg=YELLOW)
instruction_text.grid(column=1, row=1)

Label(text="Write your text here: ", bg=YELLOW).grid(column=0, row=3)

user_input = Entry(width=22)
user_input.grid(column=1, row=3)
user_input.focus()
user_input.bind("<Return>", check_typing)

check_button = Button(text="Check", command=check_typing, bg=YELLOW, highlightthickness=0,)
check_button.grid(column=1, row=4)

start_button = Button(text="Start", bg=YELLOW, highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=5)

reset_button = Button(text="Reset", bg=YELLOW,highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=5)


window.mainloop()