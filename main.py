from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import os


def generate_password():
    """Creates a random unique password"""

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    word = [choice(letters) for _ in range(randint(10, 12))]
    sym = [choice(symbols) for _ in range(randint(4, 6))]
    num = [choice(numbers) for _ in range(randint(4, 6))]

    combine = word + sym + num
    shuffle(combine)
    password = "".join(combine)

    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


def add_button_func():
    """This is the function that is carried out when the add button is pressed. it writes the data into the appropriate
    files"""

    web = website_input.get()
    website = website_input.get().lower()
    email_user = email_user_input.get().lower()
    password = password_input.get()
    contents = [website, email_user, password]
    new_data = {
        website: {
            "email": email_user,
            "password": password,
        }
    }

    if not os.path.exists("instance"):
        os.makedirs("instance")

    def is_env():
        """Writes the data into an env file located in instance/.env"""
        with open("instance/.env", "contents") as env_file:
            new_website = website.replace(" ", "_")
            env_file.write(f"{new_website}='{password}'\n")

    def is_coupon():
        """Writes the data into the coupon file located in instance/coupon"""
        with open("instance/coupon", "contents") as env_file:
            new_website = website.replace(" ", "_")
            env_file.write(f"{new_website}='{password}'\n")

    def add_json():
        """Writes the data into contents json file located in instance/data.json"""
        try:
            with open("instance/data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("instance/data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("instance/data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

    if "" in contents:
        messagebox.showinfo(title="Oops", message="Please fill in all the required entries")
    else:
        is_ok = messagebox.askokcancel(title=web,
                                       message=f"These are the details entered:\nEmail/Username: "
                                               f"{email_user}\nPassword: {password}\nIs it OK to save?")
        if is_ok:
            if checked_state.get():
                is_env()
                add_json()
            if checked_state_2.get():
                is_coupon()
            else:
                add_json()

            website_input.delete(0, END)
            password_input.delete(0, END)


def search():
    """Searches the json file for the required data the user is requesting"""
    website = website_input.get().lower()
    web = website_input.get()
    if website == "":
        messagebox.showinfo(title="Oops", message="Please fill in the Website field")
    else:
        try:
            with open("instance/data.json", "r") as data_file:
                data = json.load(data_file)
                if website in data:
                    email = data[website]["email"]
                    password = data[website]["password"]
                    messagebox.showinfo(title=web, message=f"Email/Username: {email}\nPassword: {password}")
                    pyperclip.copy(password)
                else:
                    messagebox.showinfo(title="Oops", message=f"Sorry no website matching '{web}' was found")

        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No Data File Found")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=75)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_user_label = Label(text="Email/Username:")
email_user_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)


# entries
website_input = Entry(width=34)
website_input.focus()
website_input.grid(row=1, column=1)

email_user_input = Entry(width=52)
email_user_input.insert(0, "joeuzoproject@gmail.com")
email_user_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=34)
password_input.grid(row=3, column=1)

# buttons
search_button = Button(text="Search", width=14, highlightthickness=1, command=search)
search_button.grid(row=1, column=2)

generate_password_button = Button(text="Generate Password", width=14, highlightthickness=1, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(width=44, text="Add", highlightthickness=0, command=add_button_func)
add_button.grid(row=6, column=1, columnspan=2)

# checkbutton for env
checked_state = BooleanVar()
checkbutton = Checkbutton(text="Environmental Variable", variable=checked_state)
checked_state.get()
checkbutton.grid(column=1, row=4, sticky="w")

# checkbutton for coupon
checked_state_2 = BooleanVar()
checkbutton_2 = Checkbutton(text="Coupon", variable=checked_state_2)
checked_state_2.get()
checkbutton_2.grid(column=1, row=5, sticky="w")

window.mainloop()
