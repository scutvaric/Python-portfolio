from tkinter import *
from tkinter import messagebox
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
LENGTH_IN_SEC = 10
timer = None





# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    if 'timer' in globals() and timer is not None:
        window.after_cancel(timer)

    canvas.itemconfig(timer_text, text="00:10")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer(event=None):
    if timer is not None:
        window.after_cancel(timer)
    count_down(LENGTH_IN_SEC)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60

    canvas.itemconfig(timer_text, text=f"{count_min:02}:{count_sec:02}")

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        window.update()
        reset_timer()
        messagebox.showinfo(title="Time's up", message="You waited too long before typing. All progress is lost!")
        user_input.delete("1.0", END)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Text writing app")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width=120, height=50, bg=YELLOW, highlightthickness=0)
timer_text = canvas.create_text(60, 25, text="00:10", fill="black", font=(FONT_NAME, 35,"bold"))
canvas.grid(column=1, row=0)


instruction_text = Label(text="↓ Write your text below, if you don't write anything in 10 seconds"
                              " all your progress will be lost ↓", bg=YELLOW)
instruction_text.grid(column=1, row=1)

user_input = Text(width=100, height=20)
user_input.grid(column=1, row=3)
user_input.focus()
user_input.bind("<KeyRelease>", start_timer)


window.mainloop()