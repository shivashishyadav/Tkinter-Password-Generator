from tkinter import *
from tkinter import messagebox
import string, random, pyperclip, json

window = Tk()
window.geometry("510x360")
window.config(padx=20, pady=20)
window.title("Password Generator")

ALL_LABEL_FONT = ("Arial", 11, "bold")
ALL_BUTTON_FONT = ("Arial", 8, "bold")
ALL_ENTRY_FONT = ("Arial", 10, "bold")
TOMATO = "tomato"


# clear all fields
def clear_fields():
    website_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)
    website_entry.focus_set()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    lower_case_alphabet = list(string.ascii_lowercase)
    upper_case_alphabet = list(string.ascii_uppercase)
    digits = list(string.digits)
    symbols = ["!", "#", "$", "%", "*", "_", "@"]

    lower_letter = [random.choice(lower_case_alphabet) for _ in range(4)]
    upper_letter = [random.choice(upper_case_alphabet) for _ in range(3)]
    digit = [random.choice(digits) for _ in range(3)]
    symbol = [random.choice(symbols) for _ in range(4)]

    password_list = lower_letter + upper_letter + digit + symbol
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVING RECORDS JSON FORMAT ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) < 4 or len(email) < 5 or len(password) < 6:
        messagebox.showinfo(
            title="Requirement not full filled",
            message="Envalid Email or Password or Website\nPlease Try again..",
        )
    else:
        # CATCH THE EXCEPTION
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            clear_fields()


# ---------------------------- SEARCHING THE STORED RECORD ------------------------------- #
def search():
    website = website_entry.get().capitalize()
    try:
        with open("data.json", "r") as data_file:
            account_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File not found")
    else:
        if website in account_data:
            email = account_data[website]["email"]
            password = account_data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Email: {email}\nPassword: {password}",
            )
        else:
            messagebox.showinfo(title="Error", message=f"{website} info is not found")
    finally:
        clear_fields()


# ---------------------------- UI SETUP ------------------------------- #

# Rendering the image onto the canvas
canvas = Canvas(width=200, height=200)
my_file = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=my_file)
canvas.grid(row=0, column=1)

# Creating all text label
website_name_label = Label(text="Website Name:", font=ALL_LABEL_FONT, fg=TOMATO)
website_name_label.grid(row=1, column=0, sticky="w")
email_username_label = Label(text="Email/Username:", font=ALL_LABEL_FONT, fg=TOMATO)
email_username_label.grid(row=2, column=0, sticky="w")
password_label = Label(text="Password:", font=ALL_LABEL_FONT, fg=TOMATO)
password_label.grid(row=3, column=0, sticky="w")

# creating all the entry fields
website_entry = Entry(width=28, font=ALL_ENTRY_FONT, bg="ivory")
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=46, font=ALL_ENTRY_FONT, bg="ivory")
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=28, font=ALL_ENTRY_FONT, bg="ivory")
password_entry.grid(row=3, column=1)

# Creating button for application
search_button = Button(
    text="Search",
    width=16,
    font=ALL_BUTTON_FONT,
    bg=TOMATO,
    command=search,
)
search_button.grid(row=1, column=2)
generate_button = Button(
    text="Generate Password",
    font=ALL_BUTTON_FONT,
    command=password_generator,
    bg=TOMATO,
)
generate_button.grid(row=3, column=2)
add_button = Button(
    width=45,
    text="+Add",
    font=ALL_BUTTON_FONT,
    command=save,
    bg=TOMATO,
)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
