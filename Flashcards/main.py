from tkinter import *
import pandas
import random

BG_COLOR = "#B1DDC6"

word_pair = {}
to_learn = {}


def next_card():
    global word_pair, flip_timer
    window.after_cancel(flip_timer)

    word_pair = random.choice(to_learn)

    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=word_pair["French"], fill="black")

    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=word_pair["English"], fill="white")


def remove_card():
    to_learn.remove(word_pair)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)

    next_card()


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BG_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BG_COLOR, highlightthickness=0)

cross_image = PhotoImage(file="images/wrong.png")
check_image = PhotoImage(file="images/right.png")
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong_button = Button(image=cross_image, highlightthickness=0, bd=0, command=next_card)
wrong_button.grid(column=0, row=1)
right_button = Button(image=check_image, highlightthickness=0, bd=0, command=remove_card)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
