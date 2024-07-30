# Not secure, passwords stored in plaintext! 

from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------------- SEARCH ------------------------------------- #
def search():
    website = website_entry.get().lower()
    try:
        with open("saved passwords.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="File not found!")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email/Username: {email}\n"f"Password: {password}")
        else:
            messagebox.showinfo(title="Oops", message=f"No details for {website} exists.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    generated_password = "".join(password_list)
    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password
        }
    }

    if website == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        return

    try:
        with open("saved passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        with open("saved passwords.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        data.update(new_data)
        with open("saved passwords.json", "w") as file:
            json.dump(data, file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_button = Button(text="Search", command=search, width=14)
search_button.grid(column=2, row=1)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

email_username_entry = Entry(width=52)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "andrew@email.com")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

generate = Button(text="Generate Password", command=generate_password)
generate.grid(column=2, row=3)

add = Button(text="Add", width=44, command=save)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
