import tkinter as tk

import hashlib

# ---------- Function to the principal page ----------
def home():
    global text, home_frame
    home_frame = tk.Frame(window)
    home_frame.pack()
    veranera = tk.Label(home_frame, text = "Welcome to Veranera!", font = ("Verdana", 18))
    veranera.pack()
    sign_in = tk.Button(home_frame, text = "Sign in", command = signin)
    sign_in.pack()
    sign_up = tk.Button(home_frame, text = "Sign up", command = signup)
    sign_up.pack()
    text = tk.Label(home_frame, text = "", font = ("Verdana", 10))
    text.pack()

# Function to enter the email
def enter_email():
    global the_email, email_error, email_text, register_frame
    home_frame.pack_forget() # Deletes the home elements
    register_frame = tk.Frame(window)
    register_frame.pack()
    email_text = tk.Label(register_frame, text = "Email:")
    email_text.pack()
    the_email = tk.Entry(register_frame, width = 22)
    the_email.pack()
    email_error = tk.Label(register_frame, text = "")
    email_error.pack()

# Function to delete the text of the email
def empty_email():
    the_email.delete(0, len(the_email.get()))
    the_email.insert(0, "")

# Function to show the password entry
def enter_password():
    global pass_text, the_pass
    next.pack_forget()
    the_email.pack_forget()
    pass_text = tk.Label(register_frame, text = "Password:")
    pass_text.pack()
    the_pass = tk.Entry(register_frame, width = 22, show = "*")
    the_pass.pack()
    pass_error = tk.Label(register_frame, text = "")
    pass_error.pack()

# Function to delete text of the password
def empty_pass():
    the_pass.delete(0, len(the_email.get()))
    the_pass.insert(0, "")
    confirm_pass.delete(0, len(the_email.get()))
    confirm_pass.insert(0, "")

# ---------- Function to log in ----------
def signin():
    global next
    enter_email()
    next = tk.Button(register_frame, text = "Next", command = verify_email)
    next.pack()

# Function to verify if the email exists
def verify_email():
    global pin, pass_error
    email = the_email.get()
    with open('registered_accounts.txt', 'r') as email_file:
        accounts_list = email_file.readlines()
        for line in range(0, len(accounts_list)):
            account = accounts_list[line].split()
            user = account[0]
            pin = account[1]
            if user == email:
                email_error.config(text = email)
                enter_password()
                pass_error = tk.Label(register_frame, text = "")
                pass_error.pack()
                log_in = tk.Button(register_frame, text = "Log in", command = verify_password)
                log_in.pack()
                break
        if user != email:
            email_error.config(text = "- Email not founded")

# Function to verify if the password it's corrects
def verify_password():
    password = the_pass.get()
    if password == pin:
        pass_error.config(text = "- Correct!")
    else:
        pass_error.config(text = "- Incorrect password")
        the_pass.delete(0, len(the_email.get()))
        the_pass.insert(0, "")

# ---------- Function to register ----------
def signup():
    global next
    enter_email()
    next = tk.Button(register_frame, text = "Next", command = create_email)
    next.pack()

# Function to create an email
def create_email():
    global email, confirm_text, pass_error, confirm_pass
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
            empty_email()
        elif counter == 2:
            email_error.config(text = "- Invalid username")
            empty_email()
        elif counter == 3:
            email_error.config(text = "- Invalid domain")
            empty_email()
        else:
            email_error.config(text = email)
            enter_password()
            confirm_text = tk.Label(register_frame, text = "Confirm password:")
            confirm_text.pack()
            confirm_pass = tk.Entry(register_frame, width = 22, show = "*")
            confirm_pass.pack()
            pass_error = tk.Label(register_frame, text = "")
            pass_error.pack()
            register = tk.Button(register_frame, text = "Register", command = create_password)
            register.pack()
    except:
        empty_email()
        email_error.config(text = "- Error, try again")

# Function to create a password
def create_password():
    global password
    password = the_pass.get()
    confirm = confirm_pass.get()
    if password == confirm:
        if password_strength():

            hash = hashlib.sha256(password.encode("utf-8"))
            with open('registered_accounts.txt', 'a', encoding="utf-8") as register_file:
                register_file.write(f"{email} {password} {hash.hexdigest()}\n")
            register_frame.pack_forget()
            home()
            text.config(text = "- You account was created succesfully!")
        else:
            pass_error.config(text = "- Weak password")
            empty_pass()
    else:
        pass_error.config(text = "- Passwords don't match")
        empty_pass()

# Function to verify the strenght of the password
def password_strength():
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

# ---------- This is where the code starts running ----------
if __name__ == '__main__':
    # Create the window
    window = tk.Tk()
    window.title("Cafetería: veranera")
    window.geometry("300x300")
    window.resizable(False, False)
    home()
    window.mainloop()