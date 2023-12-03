import tkinter as tk

import hashlib

# Function to the principal page
def home():
    global veranera, sign_in, sign_up, text
    veranera = tk.Label(window, text = "Welcome to Veranera!", font = ("Verdana", 18))
    veranera.pack()
    sign_in = tk.Button(window, text = "Sign in")
    sign_in.pack()
    sign_up = tk.Button(window, text = "Sign up", command = signup)
    sign_up.pack()
    text = tk.Label(window, text = "", font = ("Verdana", 10))
    text.pack()


# Function to sign up
def signup():
    global the_email, signup_pass, email_error, email_text
    veranera.pack_forget()
    sign_in.pack_forget()
    sign_up.pack_forget()
    email_text = tk.Label(window, text = "Email:")
    email_text.pack()
    the_email = tk.Entry(window, width = 22)
    the_email.pack()
    email_error = tk.Label(window, text = "")
    email_error.pack()
    next = tk.Button(window, text = "Next", command = create_email)
    next.pack()
    def signup_pass():
        global the_pass, pass_error, confirm_pass, pass_text, confirm_text, register
        next.pack_forget()
        the_email.pack_forget()
        pass_text = tk.Label(window, text = "Password:")
        pass_text.pack()
        the_pass = tk.Entry(window, width = 22, show = "*")
        the_pass.pack()
        confirm_text = tk.Label(window, text = "Confirm password:")
        confirm_text.pack()
        confirm_pass = tk.Entry(window, width = 22, show = "*")
        confirm_pass.pack()
        pass_error = tk.Label(window, text = "")
        pass_error.pack()
        register = tk.Button(window, text = "Register", command = create_password)
        register.pack()

# Function to create an email
def create_email():
    global email, the_email, email_error
    email_digits = "abcdefghijklmnopqrstuvwxyz0123456789._"
    valid_domains = ["@gmail.com", "@hotmail.com", "@yahoo.com",
                    "@outlook.com", "@correounivalle.edu.co"]

    counter = 0
    try:
        email = the_email.get()
        username = email[0:email.index("@")]
        domain = email[email.index("@"):len(email)]
        with open('registered_accounts.txt', 'r') as email_file:
            accounts_list = email_file.readlines()
            for line in range(0, len(accounts_list)):
                account = accounts_list[line].split()
                user = account[0]
                pin = account[1]
                if user == email:
                    counter = 1
                    continue
        for word in username:
            if word not in email_digits:
                counter = 2
            elif len(username) < 6 or len(username) > 30:
                counter = 2
            elif domain not in valid_domains:
                counter = 3
        if counter == 1:
            email_error.config(text = "- The email already exists")
        elif counter == 2:
            email_error.config(text = "- Invalid username")
        elif counter == 3:
            email_error.config(text = "- Invalid domain")
        else:
            email_error.config(text = email)
            signup_pass()
    except:
        email_error.config(text = "- Error, try again")


# Function to create a password
def create_password():
    global password, h, email
    password = the_pass.get()
    confirm = confirm_pass.get()
    if password == confirm:
        if password_strength():

            hash = hashlib.sha256(password.encode("utf-8"))
            with open('registered_accounts.txt', 'a', encoding="utf-8") as register_file:
                register_file.write(f"{email} {password} {hash.hexdigest()}\n")
            email_text.pack_forget()
            the_email.pack_forget()
            email_error.pack_forget()
            pass_text.pack_forget()
            the_pass.pack_forget()
            confirm_text.pack_forget()
            confirm_pass.pack_forget()
            pass_error.pack_forget()
            register.pack_forget()
            home()
            text.config(text = "- You account was created succesfully!")
        else:
            pass_error.config(text = "- Weak password")
    else:
        pass_error.config(text = "- Passwords don't match")


# Function to verify the strenght of the password
def password_strength():
    global password
    low = False
    up = False
    simbol = False
    number = False
    for caracter in password:
        if caracter.islower():
            low = True
        elif caracter.isupper():
            up = True
        elif caracter.isdigit():
            number = True
        elif caracter in "@*$!?\&/.-_":
            simbol = True
    return low and up and number and simbol and len(password) >= 10


if __name__ == '__main__':
    # Create the window
    window = tk.Tk()
    window.title("Cafetería: veranera")
    window.geometry("300x300")
    window.resizable(False, False)
    home()
    window.mainloop()