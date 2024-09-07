""" Rules:
Card changes every 3 seconds to the eng translation. Click tick if you got the answer right, cross if you
didn't.

"""

from tkinter import *
from random import *
import pandas
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# French Words Data
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)  # random word from the current list
    french_words = current_card["French"]  # random values from French Key
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_words, fill="black")
    canvas.itemconfig(card_background, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False) # Index numbers are not created
    next_card()


# Window
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# PhotoImages
card_back = PhotoImage(file="./images/card_back.png")
card_front = PhotoImage(file="./images/card_front.png")

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_background = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 40, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


# Buttons (open buttons and set coordinates; then done)
cross = PhotoImage(file="./images/wrong.png")
red_button = Button(image=cross, highlightthickness=0, command=next_card)
red_button.grid(row=1, column=0)

tick = PhotoImage(file="./images/right.png")
green_button = Button(image=tick, highlightthickness=0, command=is_known)
green_button.grid(row=1, column=1)

next_card()    # Generates the first card when the game starts

canvas.mainloop()
